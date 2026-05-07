import asyncio
from app.services.ai.gemini_client import generate_score_explanation, generate_outreach_email
from app.config import settings

async def main():
    print(f"Key loaded: {settings.gemini_api_key is not None and bool(settings.gemini_api_key.strip())}")
    
    company = {
        "name": "Chicago HVAC Doctor",
        "industry_description": "HVAC",
        "founded_year": 1990,
        "hq_city": "Chicago",
        "hq_state": "IL",
        "owner_name": "Bob Smith"
    }
    score = {
        "total": 85,
        "tier": "Tier 1",
        "breakdown": {"financial_fit": 20, "operational_profile": 20}
    }
    
    try:
        res = await generate_score_explanation(company, score)
        print("Exp:\n", res)
    except Exception as e:
        print("Exp Error:", e)

    try:        
        email = await generate_outreach_email(company, score)
        print("Email:\n", email)
    except Exception as e:
        print("Email Error:", e)

if __name__ == "__main__":
    asyncio.run(main())
