"""
Tests for website scraper and Hunter.io enrichment services.
All external HTTP calls are mocked.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


# ── Website Scraper ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_scraper_extracts_founded_year_explicit():
    from app.services.enrichment.website_scraper import scrape_company_website
    html = "<html><body><p>Founded in 1998, Acme HVAC has served Dallas for over 25 years.</p></body></html>"
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = html
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await scrape_company_website("https://acmehvac.com")
    assert result.get("founded_year") == 1998

@pytest.mark.asyncio
async def test_scraper_extracts_established_year():
    from app.services.enrichment.website_scraper import scrape_company_website
    html = "<html><body><p>Established 2003 serving the greater Phoenix area.</p></body></html>"
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = html
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await scrape_company_website("https://example.com")
    assert result.get("founded_year") == 2003

@pytest.mark.asyncio
async def test_scraper_fallback_to_earliest_year():
    from app.services.enrichment.website_scraper import scrape_company_website
    html = "<html><body><p>Copyright 1995. Contact us at 2024 Main St.</p></body></html>"
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = html
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await scrape_company_website("https://example.com")
    assert result.get("founded_year") == 1995

@pytest.mark.asyncio
async def test_scraper_extracts_employee_count():
    from app.services.enrichment.website_scraper import scrape_company_website
    html = "<html><body><p>Our team of 45 technicians serves the Dallas area.</p></body></html>"
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = html
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await scrape_company_website("https://example.com")
    assert result.get("employee_count_low") is not None
    assert result.get("employee_count_high") is not None
    assert result["employee_count_low"] <= 45 <= result["employee_count_high"]

@pytest.mark.asyncio
async def test_scraper_extracts_meta_description():
    from app.services.enrichment.website_scraper import scrape_company_website
    html = '<html><head><meta name="description" content="Dallas HVAC contractor since 1998"></head><body></body></html>'
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = html
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await scrape_company_website("https://example.com")
    assert "Dallas HVAC contractor" in result.get("website_description", "")

@pytest.mark.asyncio
async def test_scraper_returns_empty_for_empty_url():
    from app.services.enrichment.website_scraper import scrape_company_website
    result = await scrape_company_website("")
    assert result == {}

@pytest.mark.asyncio
async def test_scraper_returns_empty_on_http_error():
    from app.services.enrichment.website_scraper import scrape_company_website
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.text = ""
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await scrape_company_website("https://example.com/404")
    assert result == {}

@pytest.mark.asyncio
async def test_scraper_returns_empty_on_connection_error():
    from app.services.enrichment.website_scraper import scrape_company_website
    import httpx
    with patch("httpx.AsyncClient") as MockClient:
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(side_effect=httpx.ConnectError("refused"))
        result = await scrape_company_website("https://dead.example.com")
    assert result == {}

@pytest.mark.asyncio
async def test_scraper_out_of_range_year_uses_fallback():
    """When FOUNDED_PATTERN matches but year is out of range, fallback should still run."""
    from app.services.enrichment.website_scraper import scrape_company_website
    # "Founded in 1800" is out of range (< 1950), but "since 1987" is in the text too
    html = "<html><body><p>Founded in 1800 — our family. Operating since 1987.</p></body></html>"
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = html
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await scrape_company_website("https://example.com")
    # The explicit "Founded in 1800" is out-of-range, so fallback to YEAR_PATTERN finds 1987
    assert result.get("founded_year") == 1987


# ── Hunter.io ────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_hunter_returns_empty_for_empty_domain():
    from app.services.enrichment.hunter import find_owner_email
    result = await find_owner_email("")
    assert result == {}

@pytest.mark.asyncio
async def test_hunter_returns_empty_when_no_api_key(monkeypatch):
    from app.services.enrichment import hunter
    from app.config import settings
    monkeypatch.setattr(settings, "hunter_api_key", "")
    result = await hunter.find_owner_email("example.com")
    assert result == {}

@pytest.mark.asyncio
async def test_hunter_prioritizes_owner_title():
    from app.services.enrichment.hunter import find_owner_email
    mock_data = {
        "data": {
            "emails": [
                {"value": "sales@acme.com", "position": "Sales Manager",
                 "first_name": "Bob", "last_name": "Jones", "confidence": 80},
                {"value": "john@acme.com", "position": "Owner",
                 "first_name": "John", "last_name": "Smith", "confidence": 90},
            ]
        }
    }
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await find_owner_email("acme.com")
    assert result["owner_email"] == "john@acme.com"
    assert result["owner_name"] == "John Smith"

@pytest.mark.asyncio
async def test_hunter_falls_back_to_first_email_when_no_owner_title():
    from app.services.enrichment.hunter import find_owner_email
    mock_data = {
        "data": {
            "emails": [
                {"value": "info@acme.com", "position": "Marketing",
                 "first_name": "Alice", "last_name": "Brown", "confidence": 75},
            ]
        }
    }
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await find_owner_email("acme.com")
    assert result["owner_email"] == "info@acme.com"

@pytest.mark.asyncio
async def test_hunter_returns_empty_on_rate_limit():
    from app.services.enrichment.hunter import find_owner_email
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 429
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await find_owner_email("acme.com")
    assert result == {}

@pytest.mark.asyncio
async def test_hunter_returns_empty_on_no_emails():
    from app.services.enrichment.hunter import find_owner_email
    mock_data = {"data": {"emails": []}}
    with patch("httpx.AsyncClient") as MockClient:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_data
        mock_resp.raise_for_status = MagicMock()
        MockClient.return_value.__aenter__ = AsyncMock(return_value=MockClient.return_value)
        MockClient.return_value.__aexit__ = AsyncMock(return_value=False)
        MockClient.return_value.get = AsyncMock(return_value=mock_resp)
        result = await find_owner_email("acme.com")
    assert result.get("owner_email") is None
