"""
Tests for Google Places discovery service.
All HTTP calls are mocked.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


def _mock_places_response(places: list[dict]) -> dict:
    return {"places": places}


def _make_place(name="Acme HVAC", status="OPERATIONAL", has_website=True) -> dict:
    place = {
        "displayName": {"text": name},
        "formattedAddress": "123 Main St, Dallas, TX 75201",
        "nationalPhoneNumber": "214-555-1234",
        "rating": 4.5,
        "userRatingCount": 87,
        "primaryTypeDisplayName": {"text": "HVAC contractor"},
        "businessStatus": status,
    }
    if has_website:
        place["websiteUri"] = "https://acmehvac.com"
    return place


@pytest.mark.asyncio
async def test_search_returns_list_of_dicts():
    from app.services.discovery.google_places import search_businesses
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.json.return_value = _mock_places_response([_make_place()])
        mock_resp.raise_for_status = MagicMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.post = AsyncMock(return_value=mock_resp)
        results = await search_businesses("HVAC", "Dallas", "TX")
    assert isinstance(results, list)
    assert len(results) == 1


@pytest.mark.asyncio
async def test_search_extracts_required_fields():
    from app.services.discovery.google_places import search_businesses
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.json.return_value = _mock_places_response([_make_place("Best HVAC Co")])
        mock_resp.raise_for_status = MagicMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.post = AsyncMock(return_value=mock_resp)
        results = await search_businesses("HVAC", "Dallas", "TX")
    r = results[0]
    assert r["name"] == "Best HVAC Co"
    assert r["phone"] == "214-555-1234"
    assert r["google_rating"] == 4.5
    assert r["google_review_count"] == 87
    assert r["industry_description"] == "HVAC contractor"
    assert r["hq_city"] == "Dallas"
    assert r["hq_state"] == "TX"
    assert r["domain"] == "acmehvac.com"


@pytest.mark.asyncio
async def test_search_filters_closed_businesses():
    from app.services.discovery.google_places import search_businesses
    places = [
        _make_place("Open Co", status="OPERATIONAL"),
        _make_place("Closed Co", status="CLOSED_PERMANENTLY"),
    ]
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.json.return_value = _mock_places_response(places)
        mock_resp.raise_for_status = MagicMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.post = AsyncMock(return_value=mock_resp)
        results = await search_businesses("HVAC", "Dallas", "TX")
    assert len(results) == 1
    assert results[0]["name"] == "Open Co"


@pytest.mark.asyncio
async def test_search_handles_no_website():
    from app.services.discovery.google_places import search_businesses
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.json.return_value = _mock_places_response([_make_place(has_website=False)])
        mock_resp.raise_for_status = MagicMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.post = AsyncMock(return_value=mock_resp)
        results = await search_businesses("HVAC", "Dallas", "TX")
    assert results[0]["domain"] is None
    assert results[0]["website"] == ""


@pytest.mark.asyncio
async def test_search_returns_empty_on_no_places():
    from app.services.discovery.google_places import search_businesses
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {}
        mock_resp.raise_for_status = MagicMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.post = AsyncMock(return_value=mock_resp)
        results = await search_businesses("HVAC", "Dallas", "TX")
    assert results == []


def test_domain_extraction():
    from app.services.discovery.google_places import _extract_domain
    assert _extract_domain("https://www.acmehvac.com/about") == "acmehvac.com"
    assert _extract_domain("http://acmeplumbing.com") == "acmeplumbing.com"
    assert _extract_domain("") is None
    assert _extract_domain(None) is None
