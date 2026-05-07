from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.database import get_db
from app.models.company import Company
from app.models.outreach import OutreachLog
from app.schemas.search import SearchRequest
from app.schemas.company import CompanyOut
from app.services.discovery.google_places import search_businesses
from app.services.enrichment.website_scraper import scrape_company_website
from app.services.enrichment.hunter import find_owner_email
from app.services.scoring.engine import calculate_score
from app.services.ai.gemini_client import generate_score_explanation, generate_outreach_email
import asyncio
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/search", response_model=list[CompanyOut])
async def run_search(req: SearchRequest, db: AsyncSession = Depends(get_db)):
    # Clear previous search results so each run starts fresh
    await db.execute(delete(OutreachLog))
    await db.execute(delete(Company))
    await db.commit()

    try:
        raw_list = await search_businesses(req.query, req.city, req.state, req.max_results)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Discovery failed: {e}")

    results = []
    for raw in raw_list:
        company = await _enrich_and_score(raw, req.city, req.state, req.min_business_age)
        if company is not None:
            db.add(company)
            results.append(company)

    await db.commit()
    for c in results:
        await db.refresh(c)
    return results

async def _enrich_and_score(raw: dict, city: str, state: str, min_age: int) -> Company | None:
    # Parallel enrichment (all free APIs)
    scraper_data, hunter_data = await asyncio.gather(
        scrape_company_website(raw.get("website", "")),
        find_owner_email(raw.get("domain", "")),
        return_exceptions=True,
    )

    # raw already has resolved hq_city/hq_state from the discovery service;
    # only overwrite with form values if they were actually provided
    merged = {**raw, "hq_country": "US"}
    if city:
        merged["hq_city"] = city
    if state:
        merged["hq_state"] = state
    for data in [scraper_data, hunter_data]:
        if isinstance(data, dict):
            merged.update({k: v for k, v in data.items() if v is not None})

    # Age filter
    founded = merged.get("founded_year")
    if founded and (datetime.now().year - founded) < min_age:
        return None

    # Estimate revenue from employee count (scraper) or review count (proxy)
    if not merged.get("revenue_estimate_low"):
        emp_low = merged.get("employee_count_low") or 0
        emp_high = merged.get("employee_count_high") or emp_low
        if emp_low:
            rev_per_emp = 140_000
            merged["revenue_estimate_low"] = int(emp_low * rev_per_emp)
            merged["revenue_estimate_high"] = int(emp_high * rev_per_emp)
        else:
            # Proxy from Google review count: more reviews → larger operation
            reviews = merged.get("google_review_count") or 0
            if reviews >= 200:
                merged["revenue_estimate_low"] = 2_000_000
                merged["revenue_estimate_high"] = 8_000_000
            elif reviews >= 75:
                merged["revenue_estimate_low"] = 1_000_000
                merged["revenue_estimate_high"] = 3_000_000
            elif reviews >= 20:
                merged["revenue_estimate_low"] = 500_000
                merged["revenue_estimate_high"] = 1_500_000

    score = calculate_score(merged)

    # AI generation only for Tier 1 + Tier 2
    explanation, email_data = None, {}
    if score.tier in ("Tier 1", "Tier 2"):
        explanation, email_data = await asyncio.gather(
            generate_score_explanation(merged, score),
            generate_outreach_email(merged, score),
            return_exceptions=True,
        )
        if isinstance(explanation, Exception):
            print(f"[AI] score explanation failed: {explanation}")
            explanation = None
        if isinstance(email_data, Exception):
            print(f"[AI] outreach email failed: {email_data}")
            email_data = {}

    return Company(
        id=str(uuid.uuid4()),
        name=merged["name"],
        domain=merged.get("domain"),
        industry_description=merged.get("industry_description"),
        employee_count_low=merged.get("employee_count_low"),
        employee_count_high=merged.get("employee_count_high"),
        revenue_estimate_low=merged.get("revenue_estimate_low"),
        revenue_estimate_high=merged.get("revenue_estimate_high"),
        founded_year=merged.get("founded_year"),
        hq_city=merged.get("hq_city") or None,
        hq_state=merged.get("hq_state") or None,
        hq_country="US",
        incorporation_date=merged.get("incorporation_date"),
        owner_name=merged.get("owner_name"),
        owner_email=merged.get("owner_email"),
        phone=merged.get("phone"),
        address=merged.get("address"),
        website=merged.get("website"),
        google_rating=merged.get("google_rating"),
        google_review_count=merged.get("google_review_count"),
        acquisition_score=score.total,
        score_breakdown=score.breakdown,
        score_tier=score.tier,
        score_explanation=explanation if isinstance(explanation, str) else None,
        outreach_subject=email_data.get("subject") if isinstance(email_data, dict) else None,
        outreach_body=email_data.get("body") if isinstance(email_data, dict) else None,
        enrichment_status="complete",
    )
