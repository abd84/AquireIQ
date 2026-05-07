from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompanyOut(BaseModel):
    id: str
    name: str
    domain: Optional[str] = None
    industry_description: Optional[str] = None
    naics_code: Optional[str] = None
    employee_count_low: Optional[int] = None
    employee_count_high: Optional[int] = None
    revenue_estimate_low: Optional[int] = None
    revenue_estimate_high: Optional[int] = None
    founded_year: Optional[int] = None
    hq_city: Optional[str] = None
    hq_state: Optional[str] = None
    owner_name: Optional[str] = None
    owner_email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    google_rating: Optional[float] = None
    google_review_count: Optional[int] = None
    acquisition_score: Optional[float] = None
    score_tier: Optional[str] = None
    score_breakdown: Optional[dict] = None
    score_explanation: Optional[str] = None
    outreach_subject: Optional[str] = None
    outreach_body: Optional[str] = None
    enrichment_status: str = "complete"
    created_at: datetime

    model_config = {"from_attributes": True}