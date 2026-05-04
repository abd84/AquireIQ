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
        results.append({
            "name": place.get("displayName", {}).get("text", ""),
            "address": place.get("formattedAddress", ""),
            "phone": place.get("nationalPhoneNumber", ""),
            "website": place.get("websiteUri", ""),
            "domain": _extract_domain(place.get("websiteUri", "")),
            "google_rating": place.get("rating"),
            "google_review_count": place.get("userRatingCount"),
            "industry_description": place.get("primaryTypeDisplayName", {}).get("text", ""),
            "hq_city": city,
            "hq_state": state,
            "hq_country": "US",
        })
    return results

def _extract_domain(url: str) -> str | None:
    if not url:
        return None
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    return domain or None