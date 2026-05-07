from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.company import Company
from app.models.outreach import OutreachLog
from app.schemas.outreach import OutreachLogSchema
from app.services.email.smtp_client import send_outreach_email

router = APIRouter()

@router.get("/outreach")
async def list_outreach(db: AsyncSession = Depends(get_db)):
    stmt = select(OutreachLog).order_by(OutreachLog.created_at.desc())
    result = await db.execute(stmt)
    logs = result.scalars().all()
    return [OutreachLogSchema.model_validate(l) for l in logs]


@router.post("/outreach/{company_id}/queue")
async def queue_outreach(company_id: str, db: AsyncSession = Depends(get_db)):
    company = await db.get(Company, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    next_touch = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
    log = OutreachLog(
        company_id=company_id,
        contact_email=company.owner_email,
        status="queued",
        next_touch_date=next_touch,
    )
    db.add(log)
    await db.commit()
    await db.refresh(log)
    return OutreachLogSchema.model_validate(log)


@router.patch("/outreach/{log_id}/mark-sent")
async def mark_sent(log_id: str, db: AsyncSession = Depends(get_db)):
    log = await db.get(OutreachLog, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    # Load the linked company to get the draft email
    company = await db.get(Company, log.company_id)

    email_sent = False
    if company and company.outreach_body and log.contact_email:
        try:
            await send_outreach_email(
                to_email=log.contact_email,
                subject=company.outreach_subject or "Partnership Inquiry",
                body=company.outreach_body,
            )
            email_sent = True
        except Exception as exc:
            print(f"[SMTP] Failed to send to {log.contact_email}: {exc}")

    log.status = "sent"
    log.sent_at = datetime.utcnow()
    await db.commit()
    return {"status": "sent", "email_dispatched": email_sent}
