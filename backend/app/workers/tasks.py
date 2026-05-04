import asyncio
from typing import Dict, Any
from app.workers.celery_app import celery_app
from app.config import settings
from app.database import AsyncSessionLocal
from app.models.company import Company
from app.services.enrichment.website_scraper import scrape_company_website
from app.services.enrichment.opencorporates import search_company as search_opencorporates
from app.services.enrichment.hunter import find_owner_email
from app.services.scoring.engine import calculate_score, ScoreResult
from app.services.ai.gemini_client import generate_score_explanation, generate_outreach_email
from datetime import datetime

async def _run_enrichment_async(company_id: str) -> Dict[str, Any]:
    async with AsyncSessionLocal() as db:
        company = await db.get(Company, company_id)
        if not company:
            return {"status": "error", "message": "Company not found"}
        
        # Parallel enrichment
        scraper_task = scrape_company_website(company.website or "")
        opencorporates_task = search_opencorporates(company.name)
        hunter_task = find_owner_email(company.domain or "") if company.domain else asyncio.sleep(0)
        
        # Collect results
        results = await asyncio.gather(
            scraper_task, 
            opencorporates_task, 
            hunter_task,
            return_exceptions=True
        )
        
        scraper_res = results[0] if not isinstance(results[0], Exception) else {}
        oc_res = results[1] if not isinstance(results[1], Exception) else {}
        hunter_res = (results[2] if not isinstance(results[2], Exception) else {}) or {}

        # Update company object with enrichment data
        company.enrichment_sources = {
            "scraper": scraper_res,
            "opencorporates": oc_res,
            "hunter": hunter_res
        }
        
        # Map fields from enrichment to company
        if scraper_res.get("founded_year") and not company.founded_year:
            company.founded_year = scraper_res["founded_year"]
        if scraper_res.get("employee_count_low"):
            company.employee_count_low = scraper_res["employee_count_low"]
            company.employee_count_high = scraper_res["employee_count_high"]
            
        if oc_res.get("incorporation_date"):
            company.incorporation_date = oc_res["incorporation_date"]
        if "founding_officer_still_present" in oc_res:
            company.owner_name = oc_res.get('officers', [{}])[0].get('name') if oc_res.get('officers') else None
        
        if hunter_res.get("owner_email"):
            company.owner_email = hunter_res["owner_email"]
        if hunter_res.get("owner_name") and not company.owner_name:
            company.owner_name = hunter_res["owner_name"]
            
        company.last_enriched_at = datetime.utcnow()
        company.enrichment_status = "complete"

        # Calculate Score
        company_dict = {
            **company.__dict__,
            "founding_officer_still_present": oc_res.get("founding_officer_still_present")
        }
        score_result: ScoreResult = calculate_score(company_dict)
        
        company.acquisition_score = score_result.total
        company.score_tier = score_result.tier
        company.score_breakdown = score_result.breakdown
        
        # Generate AI Responses (if we have an API key, we won't strictly validate it in the worker though unless used)
        if settings.gemini_api_key:
            try:
                score_dict = {"total": score_result.total, "tier": score_result.tier, "breakdown": score_result.breakdown}
                explanation = await generate_score_explanation(company_dict, score_dict)
                company.score_explanation = explanation
                
                email = await generate_outreach_email(company_dict, score_dict)
                company.outreach_subject = email.get("subject")
                company.outreach_body = email.get("body")
            except Exception as e:
                print(f"AI Generation failed: {e}")
        
        await db.commit()
    
    return {"status": "success", "company_id": company_id}


@celery_app.task(name="enrich_company")
def enrich_company(company_id: str):
    # Run async async code inside celery synchronous task
    loop = asyncio.get_event_loop()
    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(_run_enrichment_async(company_id))