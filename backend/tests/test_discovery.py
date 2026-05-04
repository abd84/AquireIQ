import pytest
from unittest.mock import AsyncMock, patch
from app.services.discovery.google_places import search_businesses

@pytest.mark.asyncio
async def test_search_businesses_returns_list():
    mock_response = {
        "places": [
            {
                "displayName": {"text": "Acme HVAC"},
                "formattedAddress": "123 Main St, Dallas, TX 75201",
                "nationalPhoneNumber": "214-555-1234",
                "websiteUri": "https://acmehvac.com",
                "rating": 4.5,
                "userRatingCount": 87,
                "primaryTypeDisplayName": {"text": "HVAC contractor"},
            }
        ]
    }
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value.json = lambda: mock_response
        mock_post.return_value.raise_for_status = lambda: None
        results = await search_businesses(query="HVAC contractor", city="Dallas", state="TX")
    assert len(results) == 1
    assert results[0]["name"] == "Acme HVAC"
    assert results[0]["phone"] == "214-555-1234"

@pytest.mark.asyncio
async def test_website_scraper_extracts_data():
    from app.services.enrichment.website_scraper import scrape_company_website
    html = """<html><body>
        <p>Founded in 1998, Acme HVAC has served Dallas for over 25 years.</p>
        <p>Our team of 45 technicians is led by owner John Smith.</p>
        <meta name="description" content="Dallas HVAC contractor since 1998">
    </body></html>"""
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.__aenter__ = AsyncMock(return_value=mock_get.return_value)
        mock_get.return_value.__aexit__ = AsyncMock(return_value=False)
        mock_get.return_value.text = html
        mock_get.return_value.status_code = 200
        result = await scrape_company_website("https://acmehvac.com")
    assert result["founded_year"] == 1998
