import uuid
from datetime import datetime
from sqlalchemy import String, Integer, BigInteger, Numeric, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str | None] = mapped_column(String(255))
    naics_code: Mapped[str | None] = mapped_column(String(10))
    industry_description: Mapped[str | None] = mapped_column(Text)
    employee_count_low: Mapped[int | None] = mapped_column(Integer)
    employee_count_high: Mapped[int | None] = mapped_column(Integer)
    revenue_estimate_low: Mapped[int | None] = mapped_column(BigInteger)
    revenue_estimate_high: Mapped[int | None] = mapped_column(BigInteger)
    founded_year: Mapped[int | None] = mapped_column(Integer)
    hq_city: Mapped[str | None] = mapped_column(String(100))
    hq_state: Mapped[str | None] = mapped_column(String(50))
    hq_country: Mapped[str | None] = mapped_column(String(50))
    incorporation_date: Mapped[str | None] = mapped_column(String(20))
    owner_name: Mapped[str | None] = mapped_column(String(255))
    owner_email: Mapped[str | None] = mapped_column(String(255))
    owner_linkedin_url: Mapped[str | None] = mapped_column(Text)
    acquisition_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    score_breakdown: Mapped[dict | None] = mapped_column(JSON)
    score_tier: Mapped[str | None] = mapped_column(String(20))
    score_explanation: Mapped[str | None] = mapped_column(Text)
    outreach_subject: Mapped[str | None] = mapped_column(Text)
    outreach_body: Mapped[str | None] = mapped_column(Text)
    google_rating: Mapped[float | None] = mapped_column(Numeric(3, 1))
    google_review_count: Mapped[int | None] = mapped_column(Integer)
    phone: Mapped[str | None] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(Text)
    website: Mapped[str | None] = mapped_column(Text)
    enrichment_status: Mapped[str] = mapped_column(String(50), default="pending")
    enrichment_sources: Mapped[dict | None] = mapped_column(JSON)
    last_enriched_at: Mapped[datetime | None] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)