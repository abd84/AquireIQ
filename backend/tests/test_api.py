"""
Tests for all REST API endpoints.
Uses an in-memory SQLite database via the conftest fixtures.
"""
import pytest
import uuid
from datetime import datetime


def _make_company_payload(**overrides):
    return {
        "id": str(uuid.uuid4()),
        "name": "Acme HVAC Services",
        "domain": "acmehvac.com",
        "industry_description": "HVAC contractor",
        "hq_city": "Tulsa",
        "hq_state": "OK",
        "hq_country": "US",
        "founded_year": 1998,
        "employee_count_low": 20,
        "employee_count_high": 40,
        "revenue_estimate_low": 2_000_000,
        "revenue_estimate_high": 8_000_000,
        "google_rating": 4.6,
        "google_review_count": 120,
        "owner_email": "owner@acmehvac.com",
        "phone": "918-555-1234",
        "website": "https://acmehvac.com",
        "acquisition_score": 72.5,
        "score_tier": "Tier 2",
        "score_breakdown": {"financial_fit": 22, "operational_profile": 18,
                            "owner_exit_signals": 20, "market_positioning": 6,
                            "outreach_priority": 6},
        "score_explanation": "Strong candidate with good succession signals.",
        "outreach_subject": "Potential Partnership",
        "outreach_body": "Dear owner, ...",
        "enrichment_status": "complete",
        "created_at": datetime.utcnow(),
        **overrides,
    }


async def _seed_company(db_session, **overrides):
    from app.models.company import Company
    c = Company(**_make_company_payload(**overrides))
    db_session.add(c)
    await db_session.commit()
    await db_session.refresh(c)
    return c


# ── Health ────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_returns_ok(api_client):
    resp = await api_client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


# ── GET /api/companies ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_companies_empty(api_client):
    resp = await api_client.get("/api/companies")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_companies_returns_seeded_company(api_client, db_session):
    await _seed_company(db_session)
    resp = await api_client.get("/api/companies")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "Acme HVAC Services"


@pytest.mark.asyncio
async def test_list_companies_sorted_by_score_desc(api_client, db_session):
    await _seed_company(db_session, name="Low Score Co", acquisition_score=30.0, score_tier="No Fit")
    await _seed_company(db_session, name="High Score Co", acquisition_score=85.0, score_tier="Tier 1")
    resp = await api_client.get("/api/companies")
    data = resp.json()
    assert data[0]["name"] == "High Score Co"
    assert data[1]["name"] == "Low Score Co"


@pytest.mark.asyncio
async def test_list_companies_filter_by_tier(api_client, db_session):
    await _seed_company(db_session, name="Tier1 Co", acquisition_score=80.0, score_tier="Tier 1")
    await _seed_company(db_session, name="Tier2 Co", acquisition_score=60.0, score_tier="Tier 2")
    resp = await api_client.get("/api/companies?tier=Tier 1")
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "Tier1 Co"


@pytest.mark.asyncio
async def test_list_companies_filter_by_min_score(api_client, db_session):
    await _seed_company(db_session, name="High Co", acquisition_score=80.0)
    await _seed_company(db_session, name="Low Co", acquisition_score=30.0)
    resp = await api_client.get("/api/companies?min_score=50")
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "High Co"


@pytest.mark.asyncio
async def test_list_companies_filter_by_state(api_client, db_session):
    await _seed_company(db_session, name="OK Co", hq_state="OK")
    await _seed_company(db_session, name="TX Co", hq_state="TX")
    resp = await api_client.get("/api/companies?state=OK")
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "OK Co"


# ── GET /api/companies/{id} ───────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_company_by_id(api_client, db_session):
    company = await _seed_company(db_session)
    resp = await api_client.get(f"/api/companies/{company.id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Acme HVAC Services"


@pytest.mark.asyncio
async def test_get_company_returns_score_breakdown(api_client, db_session):
    company = await _seed_company(db_session)
    resp = await api_client.get(f"/api/companies/{company.id}")
    data = resp.json()
    assert "score_breakdown" in data
    assert data["score_breakdown"]["financial_fit"] == 22


@pytest.mark.asyncio
async def test_get_company_returns_404_for_unknown_id(api_client):
    resp = await api_client.get(f"/api/companies/{uuid.uuid4()}")
    assert resp.status_code == 404


# ── DELETE /api/companies/{id} ────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_company(api_client, db_session):
    company = await _seed_company(db_session)
    resp = await api_client.delete(f"/api/companies/{company.id}")
    assert resp.status_code == 204
    # Confirm it's gone
    resp2 = await api_client.get(f"/api/companies/{company.id}")
    assert resp2.status_code == 404


@pytest.mark.asyncio
async def test_delete_company_returns_404_for_unknown_id(api_client):
    resp = await api_client.delete(f"/api/companies/{uuid.uuid4()}")
    assert resp.status_code == 404


# ── POST /api/search ──────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_search_endpoint_returns_results(api_client):
    from unittest.mock import AsyncMock, patch

    mock_places = [
        {
            "name": "Best HVAC Co",
            "phone": "918-555-1111",
            "website": "https://besthvac.com",
            "domain": "besthvac.com",
            "address": "1 Main St, Tulsa, OK",
            "google_rating": 4.7,
            "google_review_count": 150,
            "industry_description": "HVAC contractor",
            "hq_city": "Tulsa",
            "hq_state": "OK",
            "hq_country": "US",
        }
    ]
    mock_scrape = {"founded_year": 1995, "employee_count_low": 18, "employee_count_high": 35}
    mock_hunter = {"owner_email": "owner@besthvac.com", "owner_name": "Jane Doe"}

    with patch("app.api.routes.search.search_businesses", new=AsyncMock(return_value=mock_places)), \
         patch("app.api.routes.search.scrape_company_website", new=AsyncMock(return_value=mock_scrape)), \
         patch("app.api.routes.search.find_owner_email", new=AsyncMock(return_value=mock_hunter)), \
         patch("app.api.routes.search.generate_score_explanation", new=AsyncMock(return_value="Strong target.")), \
         patch("app.api.routes.search.generate_outreach_email", new=AsyncMock(return_value={"subject": "Hi", "body": "Hello"})):

        resp = await api_client.post("/api/search", json={
            "query": "HVAC contractors",
            "city": "Tulsa",
            "state": "OK",
            "max_results": 5,
        })

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "Best HVAC Co"
    assert data[0]["enrichment_status"] == "complete"
    assert data[0]["acquisition_score"] is not None
    assert data[0]["owner_email"] == "owner@besthvac.com"


@pytest.mark.asyncio
async def test_search_endpoint_filters_by_min_age(api_client):
    from unittest.mock import AsyncMock, patch

    mock_places = [
        {
            "name": "Young Co",
            "website": "https://young.com",
            "domain": "young.com",
            "phone": "555-0000",
            "address": "1 St",
            "google_rating": 4.0,
            "google_review_count": 50,
            "industry_description": "Plumbing",
            "hq_city": "Dallas",
            "hq_state": "TX",
            "hq_country": "US",
        }
    ]
    mock_scrape = {"founded_year": 2020}  # only 6 years old

    with patch("app.api.routes.search.search_businesses", new=AsyncMock(return_value=mock_places)), \
         patch("app.api.routes.search.scrape_company_website", new=AsyncMock(return_value=mock_scrape)), \
         patch("app.api.routes.search.find_owner_email", new=AsyncMock(return_value={})), \
         patch("app.api.routes.search.generate_score_explanation", new=AsyncMock(return_value="")), \
         patch("app.api.routes.search.generate_outreach_email", new=AsyncMock(return_value={})):

        resp = await api_client.post("/api/search", json={
            "query": "plumbers",
            "city": "Dallas",
            "state": "TX",
            "max_results": 5,
            "min_business_age": 10,
        })

    assert resp.status_code == 200
    assert resp.json() == []  # filtered out — too young


@pytest.mark.asyncio
async def test_search_endpoint_handles_discovery_failure(api_client):
    from unittest.mock import AsyncMock, patch

    with patch("app.api.routes.search.search_businesses",
               new=AsyncMock(side_effect=Exception("Places API error"))):
        resp = await api_client.post("/api/search", json={
            "query": "HVAC",
            "city": "Tulsa",
            "state": "OK",
        })

    assert resp.status_code == 502
