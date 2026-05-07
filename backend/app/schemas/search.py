from pydantic import BaseModel
from typing import Optional, Dict

class SearchRequest(BaseModel):
    query: str
    city: str
    state: str
    min_business_age: Optional[int] = 10
    max_business_age: Optional[int] = None
    max_results: Optional[int] = 20

class CompanyResponse(BaseModel):
    id: str
    name: str
    score_tier: Optional[str]
    acquisition_score: Optional[float]
    enrichment_status: str

    class Config:
        from_attributes = True