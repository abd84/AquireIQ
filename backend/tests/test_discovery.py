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
