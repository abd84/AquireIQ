"""
Tests for industry profile lookup — both NAICS-based and keyword-based.
The keyword path is critical because Google Places never returns NAICS codes.
"""
import pytest
from app.services.scoring.industry_multiples import get_industry_profile, multiple_to_score


# ── NAICS lookup ─────────────────────────────────────────────────────────────

def test_exact_naics_match():
    multiple, fragmented, asset_light = get_industry_profile("2382")
    assert multiple == 5.5
    assert fragmented is True
    assert asset_light is True

def test_naics_prefix_match_3digit():
    # "238" is not in table, but "2382" is — with prefix_len=4 it should match
    multiple, _, _ = get_industry_profile("23821")  # 5-char, prefix 4 = "2382"
    assert multiple == 5.5

def test_dental_naics():
    multiple, fragmented, _ = get_industry_profile("6212")
    assert multiple == 8.0
    assert fragmented is True

def test_insurance_naics_highest_multiple():
    multiple, _, _ = get_industry_profile("5241")
    assert multiple == 9.0


# ── Keyword fallback (the critical path for Google Places data) ───────────────

def test_hvac_keyword():
    multiple, fragmented, asset_light = get_industry_profile(None, "HVAC contractor")
    assert multiple == 5.5
    assert fragmented is True
    assert asset_light is True

def test_plumbing_keyword():
    multiple, fragmented, asset_light = get_industry_profile(None, "Plumbing service")
    assert multiple == 5.5
    assert fragmented is True

def test_dental_keyword():
    multiple, fragmented, _ = get_industry_profile(None, "Dental clinic")
    assert multiple == 8.0

def test_dentist_keyword():
    multiple, _, _ = get_industry_profile(None, "Dentist office")
    assert multiple == 8.0

def test_orthodontist_keyword():
    multiple, _, _ = get_industry_profile(None, "Orthodontist")
    assert multiple == 8.0

def test_physician_keyword():
    multiple, _, _ = get_industry_profile(None, "Physician office")
    assert multiple == 7.0

def test_pest_control_keyword():
    multiple, fragmented, asset_light = get_industry_profile(None, "Pest control service")
    assert multiple == 6.0
    assert fragmented is True
    assert asset_light is True

def test_insurance_keyword():
    multiple, _, _ = get_industry_profile(None, "Insurance agency")
    assert multiple == 9.0

def test_roofing_keyword():
    multiple, fragmented, _ = get_industry_profile(None, "Roofing contractor")
    assert multiple == 5.0
    assert fragmented is True

def test_electrician_keyword():
    multiple, fragmented, asset_light = get_industry_profile(None, "Electrician")
    assert multiple == 5.5
    assert asset_light is True

def test_auto_repair_keyword():
    multiple, fragmented, asset_light = get_industry_profile(None, "Auto repair shop")
    assert multiple == 4.0
    assert asset_light is False

def test_restaurant_keyword():
    multiple, _, asset_light = get_industry_profile(None, "Restaurant")
    assert multiple == 3.5
    assert asset_light is False

def test_case_insensitive_keyword():
    m1, _, _ = get_industry_profile(None, "DENTAL CLINIC")
    m2, _, _ = get_industry_profile(None, "dental clinic")
    assert m1 == m2

def test_unknown_industry_returns_default():
    multiple, fragmented, asset_light = get_industry_profile(None, "Underwater basket weaving")
    assert multiple == 4.2
    assert fragmented is False
    assert asset_light is False

def test_none_inputs_return_default():
    multiple, fragmented, asset_light = get_industry_profile(None, None)
    assert multiple == 4.2

def test_naics_takes_priority_over_keyword():
    # NAICS "6212" = dental (8.0) vs description "HVAC" (5.5) — NAICS wins
    multiple, _, _ = get_industry_profile("6212", "HVAC contractor")
    assert multiple == 8.0


# ── multiple_to_score ────────────────────────────────────────────────────────

def test_multiple_to_score_high():
    assert multiple_to_score(9.0) == 8
    assert multiple_to_score(8.0) == 8

def test_multiple_to_score_mid():
    assert multiple_to_score(7.0) == 6
    assert multiple_to_score(6.0) == 6

def test_multiple_to_score_low_mid():
    assert multiple_to_score(5.0) == 4
    assert multiple_to_score(4.5) == 4

def test_multiple_to_score_low():
    assert multiple_to_score(4.0) == 2
    assert multiple_to_score(3.5) == 2
    assert multiple_to_score(1.0) == 2
