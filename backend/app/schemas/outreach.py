from pydantic import BaseModel
from typing import Optional

class OutreachLogSchema(BaseModel):
    id: str
    company_id: str
    contact_email: Optional[str] = None
    sequence_stage: int
    status: str
    next_touch_date: Optional[str] = None

    class Config:
        from_attributes = True