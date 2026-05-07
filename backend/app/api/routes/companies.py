from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyOut

router = APIRouter()

@router.get("/companies", response_model=list[CompanyOut])
async def list_companies(
    tier: str | None = Query(None),
    min_score: float | None = Query(None),
    state: str | None = Query(None),
    skip: int = 0, limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    q = select(Company).order_by(desc(Company.acquisition_score))
    if tier:      q = q.where(Company.score_tier == tier)
    if min_score: q = q.where(Company.acquisition_score >= min_score)
    if state:     q = q.where(Company.hq_state == state)
    result = await db.execute(q.offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/companies/{company_id}", response_model=CompanyOut)
async def get_company(company_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.delete("/companies/{company_id}", status_code=204)
async def delete_company(company_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Not found")
    await db.delete(company)
    await db.commit()
