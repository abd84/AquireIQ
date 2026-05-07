import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings

HUNTER_BASE = "https://api.hunter.io/v2"

@retry(stop=stop_after_attempt(2), wait=wait_exponential(min=1, max=5))
async def find_owner_email(domain: str) -> dict:
    if not domain or not settings.hunter_api_key:
        return {}
    params = {"domain": domain, "api_key": settings.hunter_api_key, "limit": 10}
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{HUNTER_BASE}/domain-search", params=params)
        if resp.status_code == 429:
            return {}
        resp.raise_for_status()
        data = resp.json()

    emails = data.get("data", {}).get("emails", [])
    owner_email = _find_best_owner_email(emails)
    return {
        "owner_email": owner_email.get("value") if owner_email else None,
        "owner_name": _build_name(owner_email) if owner_email else None,
        "email_confidence": owner_email.get("confidence") if owner_email else None,
    }

def _find_best_owner_email(emails: list[dict]) -> dict | None:
    owner_titles = ["owner", "founder", "president", "ceo", "principal", "managing"]
    for title in owner_titles:
        for email in emails:
            position = (email.get("position") or "").lower()
            if title in position:
                return email
    return emails[0] if emails else None

def _build_name(email_data: dict) -> str | None:
    first = email_data.get("first_name") or ""
    last = email_data.get("last_name") or ""
    name = f"{first} {last}".strip()
    return name or None