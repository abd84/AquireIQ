import json
from google import genai
from google.genai import types
from app.config import settings

def _get_client():
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not set")
    return genai.Client(api_key=settings.gemini_api_key)

async def generate_score_explanation(company: dict, score_result: dict) -> str:
    client = _get_client()
    prompt = f"""
    Analyze this pre-market SMB acquisition target.
    
    Company: {company.get('name')}
    Industry: {company.get('industry_description')}
    Founded: {company.get('founded_year')}
    Location: {company.get('hq_city')}, {company.get('hq_state')}
    Employees: {company.get('employee_count_low')} - {company.get('employee_count_high')}
    Revenue Estimate: ${company.get('revenue_estimate_low')} - ${company.get('revenue_estimate_high')}
    
    Succession Readiness Score: {score_result['total']}/100 ({score_result['tier']})
    Score Breakdown:
    {json.dumps(score_result['breakdown'], indent=2)}
    
    Provide a 2-3 paragraph explanation of why this company received this score. Focus on succession readiness, owner exit signals (like business age), and financial/operational fit. Be analytical and professional.
    """
    
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt,
    )
    return response.text

async def generate_outreach_email(company: dict, score_result: dict) -> dict:
    if score_result['tier'] not in ("Tier 1", "Tier 2"):
        return {"subject": "", "body": ""}
        
    client = _get_client()
    prompt = f"""
    You are an M&A partner at a private equity firm reaching out to a business owner.
    Write a 3-paragraph cold email to the owner. Do not sound salesy. 
    Frame it as a partnership/succession discussion.
    
    Owner Name: {company.get('owner_name', 'Business Owner')}
    Company: {company.get('name')}
    Industry: {company.get('industry_description')}
    Founded: {company.get('founded_year')}
    Location: {company.get('hq_city')}
    
    Respond in JSON format with exactly two keys: "subject" and "body".
    The body should have proper line breaks.
    """
    
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"subject": "Private Equity Inquiry", "body": response.text}