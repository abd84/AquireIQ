import re
import httpx
from app.config import settings

PLACES_URL = "https://places.googleapis.com/v1/places:searchText"

FIELD_MASK = ",".join([
    "places.displayName",
    "places.formattedAddress",
    "places.nationalPhoneNumber",
    "places.websiteUri",
    "places.rating",
    "places.userRatingCount",
    "places.primaryTypeDisplayName",
    "places.businessStatus",
    "places.id",
])

async def search_businesses(query: str, city: str, state: str, max_results: int = 20) -> list[dict]:
    text_query = f"{query} in {city}, {state}"
    payload = {"textQuery": text_query, "maxResultCount": min(max_results, 20)}
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": settings.google_places_api_key,
        "X-Goog-FieldMask": FIELD_MASK,
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(PLACES_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    results = []
    for place in data.get("places", []):
        if place.get("businessStatus") == "CLOSED_PERMANENTLY":
            continue
        formatted_address = place.get("formattedAddress", "")
        resolved_city, resolved_state = _resolve_location(formatted_address, city, state)
        results.append({
            "name": place.get("displayName", {}).get("text", ""),
            "address": formatted_address,
            "phone": place.get("nationalPhoneNumber", ""),
            "website": place.get("websiteUri", ""),
            "domain": _extract_domain(place.get("websiteUri", "")),
            "google_rating": place.get("rating"),
            "google_review_count": place.get("userRatingCount"),
            "industry_description": place.get("primaryTypeDisplayName", {}).get("text", ""),
            "hq_city": resolved_city,
            "hq_state": resolved_state,
            "hq_country": "US",
        })
    return results

def _resolve_location(formatted_address: str, city: str, state: str):
    """Use form inputs if provided; otherwise parse from Google's formattedAddress."""
    if city and state:
        return city, state
    # Google format: "Street, City, ST ZIP, Country"  or  "City, ST ZIP, Country"
    parts = [p.strip() for p in formatted_address.split(",")]
    parsed_city = city or ""
    parsed_state = state or ""
    if len(parts) >= 3:
        if not parsed_city:
            parsed_city = parts[-3]
        if not parsed_state:
            m = re.match(r'^([A-Z]{2})\b', parts[-2].strip())
            if m:
                parsed_state = m.group(1)
    elif len(parts) == 2 and not parsed_city:
        parsed_city = parts[0]
        m = re.match(r'^([A-Z]{2})\b', parts[1].strip())
        if m:
            parsed_state = m.group(1)
    return parsed_city or None, parsed_state or None


def _extract_domain(url: str) -> str | None:
    if not url:
        return None
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    return domain or None