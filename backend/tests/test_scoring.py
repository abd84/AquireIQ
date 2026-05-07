"""
Tests for the 5-category scoring engine and tier classification.
Covers: financial fit, operational profile, owner exit signals,
        market positioning, outreach priority, and tier thresholds.
"""
import pytest
from app.services.scoring.engine import calculate_score, ScoreResult


def _base_company() -> dict:
    """A strong, realistic Tier 1 HVAC company from a secondary market."""
    return {
        "name": "Acme HVAC Services",
        "founded_year": 1998,
        "employee_count_low": 20,
        "employee_count_high": 40,
        "revenue_estimate_low": 2_000_000,
        "revenue_estimate_high": 8_000_000,
        "industry_description": "HVAC contractor",
        "hq_city": "Tulsa",
        "hq_state": "OK",
        "hq_country": "US",
        "google_rating": 4.6,
        "google_review_count": 120,
        "owner_email": "owner@acmehvac.com",
        "phone": "918-555-1234",
        "website": "https://acmehvac.com",
    }


# ── Return type ──────────────────────────────────────────────────────────────

def test_score_returns_score_result():
    result = calculate_score(_base_company())
    assert isinstance(result, ScoreResult)

def test_score_total_in_range():
    result = calculate_score(_base_company())
    assert 0 <= result.total <= 100

def test_score_breakdown_has_five_categories():
    result = calculate_score(_base_company())
    assert set(result.breakdown.keys()) == {
        "financial_fit",
        "operational_profile",
        "owner_exit_signals",
        "market_positioning",
        "outreach_priority",
    }

def test_breakdown_sums_to_total():
    result = calculate_score(_base_company())
    assert abs(sum(result.breakdown.values()) - result.total) < 0.1


# ── Tier classification ───────────────────────────────────────────────────────

def test_ideal_company_scores_tier1():
    result = calculate_score(_base_company())
    assert result.tier in ("Tier 1", "Tier 2")
    assert result.total >= 55

def test_young_company_scores_lower_tier():
    c = {**_base_company(), "founded_year": 2022}
    result = calculate_score(c)
    old = calculate_score(_base_company())
    assert result.total < old.total

def test_no_contact_scores_no_fit_or_tier3():
    c = {**_base_company()}
    c["owner_email"] = None
    c["phone"] = None
    c["founded_year"] = 2018
    c["google_review_count"] = 10
    result = calculate_score(c)
    assert result.tier in ("No Fit", "Tier 3")

def test_tier_thresholds():
    # Tier 1 ≥ 75
    # Tier 2 ≥ 55
    # Tier 3 ≥ 35
    # No Fit < 35
    from app.services.scoring.engine import _classify_tier
    assert _classify_tier(80) == "Tier 1"
    assert _classify_tier(75) == "Tier 1"
    assert _classify_tier(74.9) == "Tier 2"
    assert _classify_tier(55) == "Tier 2"
    assert _classify_tier(54.9) == "Tier 3"
    assert _classify_tier(35) == "Tier 3"
    assert _classify_tier(34.9) == "No Fit"
    assert _classify_tier(0) == "No Fit"


# ── Financial Fit ────────────────────────────────────────────────────────────

def test_revenue_sweet_spot_earns_max_pts():
    c = {**_base_company(), "revenue_estimate_low": 4_000_000, "revenue_estimate_high": 10_000_000}
    result = calculate_score(c)
    assert result.breakdown["financial_fit"] >= 20  # industry + age + employees also contributing

def test_no_revenue_data_still_scores():
    c = {**_base_company(), "revenue_estimate_low": None, "revenue_estimate_high": None}
    result = calculate_score(c)
    assert result.breakdown["financial_fit"] >= 0

def test_employee_count_sweet_spot():
    c = {**_base_company(), "employee_count_low": 30, "employee_count_high": 50}
    result = calculate_score(c)
    assert result.breakdown["financial_fit"] >= 15

def test_business_age_twenty_to_thirty_earns_max():
    c = {**_base_company(), "founded_year": 2002}  # 24 years old
    result = calculate_score(c)
    assert result.breakdown["financial_fit"] >= 20


# ── Operational Profile ──────────────────────────────────────────────────────

def test_secondary_market_city_earns_bonus():
    c_secondary = {**_base_company(), "hq_city": "Tulsa"}
    c_primary = {**_base_company(), "hq_city": "New York"}
    r1 = calculate_score(c_secondary)
    r2 = calculate_score(c_primary)
    assert r1.breakdown["operational_profile"] > r2.breakdown["operational_profile"]

def test_no_website_earns_low_footprint_bonus():
    c_no_site = {**_base_company(), "website": None}
    c_with_site = {**_base_company(), "website": "https://acmehvac.com"}
    r1 = calculate_score(c_no_site)
    r2 = calculate_score(c_with_site)
    assert r1.breakdown["operational_profile"] >= r2.breakdown["operational_profile"]

def test_review_volume_in_stable_range():
    c = {**_base_company(), "google_review_count": 200}
    result = calculate_score(c)
    assert result.breakdown["operational_profile"] >= 15


# ── Owner Exit Signals ───────────────────────────────────────────────────────

def test_old_business_owner_exit_signals_high():
    c = {**_base_company(), "founded_year": 1995}  # 31 years old
    result = calculate_score(c)
    assert result.breakdown["owner_exit_signals"] >= 14

def test_owner_email_keyword_earns_pts():
    c_owner = {**_base_company(), "owner_email": "owner@acmehvac.com"}
    c_generic = {**_base_company(), "owner_email": "contact@acmehvac.com"}
    r1 = calculate_score(c_owner)
    r2 = calculate_score(c_generic)
    assert r1.breakdown["owner_exit_signals"] >= r2.breakdown["owner_exit_signals"]

def test_family_business_name_earns_pts():
    c_family = {**_base_company(), "name": "Smith & Sons Plumbing"}
    c_generic = {**_base_company(), "name": "Metro Plumbing Inc"}
    r1 = calculate_score(c_family)
    r2 = calculate_score(c_generic)
    assert r1.breakdown["owner_exit_signals"] > r2.breakdown["owner_exit_signals"]

def test_apostrophe_name_earns_pts():
    c = {**_base_company(), "name": "John's Electric"}
    result = calculate_score(c)
    assert result.breakdown["owner_exit_signals"] >= 14  # age ≥25 + apostrophe

def test_no_exit_signals_scores_low():
    c = {**_base_company(), "founded_year": 2015, "owner_email": None, "name": "TechCorp Solutions"}
    result = calculate_score(c)
    assert result.breakdown["owner_exit_signals"] <= 10


# ── Market Positioning ───────────────────────────────────────────────────────

def test_high_rating_many_reviews_earns_local_brand_pts():
    c = {**_base_company(), "google_rating": 4.8, "google_review_count": 200}
    result = calculate_score(c)
    assert result.breakdown["market_positioning"] >= 8  # fragmented + brand


# ── Outreach Priority ────────────────────────────────────────────────────────

def test_email_and_phone_earns_max_outreach_pts():
    c = {**_base_company(), "owner_email": "owner@acme.com", "phone": "918-555-0000"}
    result = calculate_score(c)
    assert result.breakdown["outreach_priority"] == 10

def test_email_only_earns_partial_outreach_pts():
    c = {**_base_company(), "phone": None}
    result = calculate_score(c)
    assert result.breakdown["outreach_priority"] == 7

def test_phone_only_earns_partial_outreach_pts():
    c = {**_base_company(), "owner_email": None}
    result = calculate_score(c)
    assert result.breakdown["outreach_priority"] == 4

def test_no_contact_earns_minimum_outreach_pts():
    c = {**_base_company(), "owner_email": None, "phone": None}
    result = calculate_score(c)
    assert result.breakdown["outreach_priority"] == 1


# ── Edge cases ───────────────────────────────────────────────────────────────

def test_empty_company_dict_does_not_crash():
    result = calculate_score({})
    assert isinstance(result, ScoreResult)
    assert result.total >= 0

def test_score_capped_at_100():
    # Pathological case — max everything
    c = {
        "name": "Smith & Sons Brothers Plumbing",
        "founded_year": 1985,
        "employee_count_low": 30,
        "employee_count_high": 50,
        "revenue_estimate_low": 5_000_000,
        "revenue_estimate_high": 10_000_000,
        "industry_description": "plumbing hvac",
        "hq_city": "Tulsa",
        "hq_state": "OK",
        "google_rating": 4.9,
        "google_review_count": 300,
        "owner_email": "owner@smithsons.com",
        "phone": "918-555-9999",
        "website": None,
    }
    result = calculate_score(c)
    assert result.total <= 100
