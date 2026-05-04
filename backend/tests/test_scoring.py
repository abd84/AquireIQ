import pytest
from app.services.scoring.engine import calculate_score, ScoreResult

def _base_company() -> dict:
    return {
        "founded_year": 1998,
        "employee_count_low": 20,
        "employee_count_high": 40,
        "revenue_estimate_low": 2_000_000,
        "revenue_estimate_high": 8_000_000,
        "naics_code": "2382",
        "hq_city": "Tulsa",
        "hq_state": "OK",
        "hq_country": "US",
        "google_rating": 4.6,
        "google_review_count": 120,
        "owner_email": "john@acmehvac.com",
        "incorporation_date": "1998-03-15",
        "founding_officer_still_present": True,
        "officer_count": 1,
        "website": "https://acmehvac.com",
    }

def test_score_returns_result():
    result = calculate_score(_base_company())
    assert isinstance(result, ScoreResult)
    assert 0 <= result.total <= 100

def test_high_quality_target_scores_tier1():
    result = calculate_score(_base_company())
    assert result.total >= 60
    assert result.tier in ("Tier 1", "Tier 2")

def test_young_company_scores_lower():
    company = _base_company()
    company["founded_year"] = 2021
    result = calculate_score(company)
    old_result = calculate_score(_base_company())
    assert result.total < old_result.total

def test_breakdown_sums_to_total():
    result = calculate_score(_base_company())
    breakdown_sum = sum(result.breakdown.values())
    assert abs(breakdown_sum - result.total) < 1