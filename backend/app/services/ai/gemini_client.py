import asyncio
import json
import google.generativeai as genai
from app.config import settings
from app.services.ai.prompts import score_explanation_prompt, outreach_email_prompt

_model = None  # reset on each reload

def _get_model():
    global _model
    if _model is None:
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        genai.configure(api_key=settings.gemini_api_key)
        _model = genai.GenerativeModel("gemini-2.5-flash")
    return _model


async def generate_score_explanation(company: dict, score_result) -> str:
    score_total = score_result.total if hasattr(score_result, 'total') else score_result.get('total')
    score_tier = score_result.tier if hasattr(score_result, 'tier') else score_result.get('tier')
    score_breakdown = score_result.breakdown if hasattr(score_result, 'breakdown') else score_result.get('breakdown', {})

    model = _get_model()
    prompt = score_explanation_prompt(company, score_total, score_tier, score_breakdown)
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


async def generate_outreach_email(company: dict, score_result) -> dict:
    score_tier = score_result.tier if hasattr(score_result, 'tier') else score_result.get('tier')

    if score_tier not in ("Tier 1", "Tier 2"):
        return {"subject": "", "body": ""}

    model = _get_model()
    prompt = outreach_email_prompt(company)

    def _call():
        return model.generate_content(
            contents=prompt,
            generation_config=genai.GenerationConfig(response_mime_type="application/json"),
        )

    response = await asyncio.to_thread(_call)
    try:
        return json.loads(response.text)
    except Exception:
        return {"subject": "Private Equity Inquiry", "body": response.text}
