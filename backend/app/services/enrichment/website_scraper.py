import re
import httpx
from bs4 import BeautifulSoup

YEAR_PATTERN = re.compile(r'\b(19[6-9]\d|20[0-2]\d)\b')
EMPLOYEE_PATTERN = re.compile(r'\b(\d{1,4})\s*(employees?|technicians?|staff|team members?|professionals?)\b', re.IGNORECASE)
FOUNDED_PATTERN = re.compile(r'(?:founded|established|since|serving since|in business since)\s+(?:in\s+)?(\d{4})', re.IGNORECASE)

async def scrape_company_website(url: str) -> dict:
    if not url:
        return {}
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (compatible; AcquireIQ/1.0)"}) as client:
            resp = await client.get(url)
            if resp.status_code >= 400:
                return {}
            html = resp.text
    except Exception:
        return {}

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)

    result = {}

    # Founded year — try explicit pattern first, fall back to earliest plausible year mention
    founded_match = FOUNDED_PATTERN.search(text)
    if founded_match:
        year = int(founded_match.group(1))
        if 1950 <= year <= 2020:
            result["founded_year"] = year

    if not result.get("founded_year"):
        years = [int(y) for y in YEAR_PATTERN.findall(text) if 1950 <= int(y) <= 2020]
        if years:
            result["founded_year"] = min(years)

    # Employee count hint
    emp_match = EMPLOYEE_PATTERN.search(text)
    if emp_match:
        count = int(emp_match.group(1))
        result["employee_count_low"] = max(1, int(count * 0.8))
        result["employee_count_high"] = int(count * 1.2)

    # Meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        result["website_description"] = meta_desc["content"][:500]

    # Title
    title = soup.find("title")
    if title:
        result["website_title"] = title.get_text(strip=True)[:200]

    return result