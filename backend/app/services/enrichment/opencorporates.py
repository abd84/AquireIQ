import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings

BASE = "https://api.opencorporates.com/v0.4"

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
async def search_company(name: str, jurisdiction: str = "us") -> dict:
    params = {
        "q": name,
        "jurisdiction_code": jurisdiction,
        "api_token": settings.opencorporates_api_token,
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{BASE}/companies/search", params=params)
        resp.raise_for_status()
        data = resp.json()

    companies = data.get("results", {}).get("companies", [])
    if not companies:
        return {}

    top = companies[0]["company"]
    officers = await _get_officers(top.get("company_number", ""), top.get("jurisdiction_code", ""))
    return {
        "incorporation_date": top.get("incorporation_date"),
        "company_status": top.get("current_status"),
        "officers": officers,
        "founding_officer_still_present": _check_founding_officer(officers),
    }

async def _get_officers(company_number: str, jurisdiction: str) -> list[dict]:
    if not company_number:
        return []
    params = {"api_token": settings.opencorporates_api_token}
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(
            f"{BASE}/companies/{jurisdiction}/{company_number}/officers", params=params
        )
        if resp.status_code != 200:
            return []
        data = resp.json()
    return [
        {
            "name": o["officer"].get("name"),
            "role": o["officer"].get("position"),
            "start_date": o["officer"].get("start_date"),
            "end_date": o["officer"].get("end_date"),
        }
        for o in data.get("results", {}).get("officers", [])
    ]

def _check_founding_officer(officers: list[dict]) -> bool:
    active = [o for o in officers if not o.get("end_date")]
    if not active:
        return False
    earliest = min(
        (o["start_date"] for o in active if o.get("start_date")),
        default=None
    )
    if not earliest:
        return False
    from datetime import datetime
    start_year = int(earliest[:4])
    return start_year <= datetime.now().year - 15