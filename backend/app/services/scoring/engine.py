from dataclasses import dataclass, field
from datetime import datetime
from app.services.scoring.industry_multiples import get_industry_profile, multiple_to_score

@dataclass
class ScoreResult:
    total: float
    tier: str
    breakdown: dict = field(default_factory=dict)

CURRENT_YEAR = datetime.now().year
TIER_1_CITIES = {"new york", "san francisco", "los angeles", "seattle", "boston",
                  "austin", "miami", "chicago", "washington", "denver"}

def calculate_score(company: dict) -> ScoreResult:
    breakdown = {}
    breakdown["financial_fit"] = _score_financial_fit(company)
    breakdown["operational_profile"] = _score_operational(company)
    breakdown["owner_exit_signals"] = _score_owner_exit(company)
    breakdown["market_positioning"] = _score_market(company)
    breakdown["outreach_priority"] = _score_outreach(company)

    total = sum(breakdown.values())
    tier = _classify_tier(total)
    return ScoreResult(total=round(total, 1), tier=tier, breakdown=breakdown)

def _score_financial_fit(c: dict) -> float:
    score = 0.0
    # Revenue range (10 pts)
    rev_low = c.get("revenue_estimate_low") or 0
    rev_high = c.get("revenue_estimate_high") or 0
    rev_mid = (rev_low + rev_high) / 2 if rev_high else rev_low
    if 3_000_000 <= rev_mid <= 12_000_000:
        score += 10
    elif 1_000_000 <= rev_mid < 3_000_000 or 12_000_000 < rev_mid <= 20_000_000:
        score += 7
    elif rev_mid > 0:
        score += 3

    # Employee count (5 pts)
    emp_mid = ((c.get("employee_count_low") or 0) + (c.get("employee_count_high") or 0)) / 2
    if 15 <= emp_mid <= 75:
        score += 5
    elif 10 <= emp_mid < 15 or 75 < emp_mid <= 150:
        score += 3
    elif emp_mid > 0:
        score += 1

    # Industry multiple (8 pts)
    multiple, _, _ = get_industry_profile(c.get("naics_code"))
    score += multiple_to_score(multiple)

    # Business age (7 pts)
    founded = c.get("founded_year")
    if founded:
        age = CURRENT_YEAR - founded
        if 20 <= age <= 30:
            score += 7
        elif 15 <= age < 20 or 30 < age <= 40:
            score += 5
        elif 10 <= age < 15:
            score += 3
        else:
            score += 1

    return min(score, 30)

def _score_operational(c: dict) -> float:
    score = 0.0
    # Asset-light (7 pts)
    _, _, is_asset_light = get_industry_profile(c.get("naics_code"))
    score += 7 if is_asset_light else 3

    # Stable (not hypergrowth) — use review growth proxy (8 pts)
    reviews = c.get("google_review_count") or 0
    if 50 <= reviews <= 500:
        score += 8
    elif reviews > 500:
        score += 5
    elif reviews > 0:
        score += 3

    # Secondary market (5 pts)
    city = (c.get("hq_city") or "").lower()
    if city and city not in TIER_1_CITIES:
        score += 5
    else:
        score += 2

    # Low digital footprint (5 pts)
    website = c.get("website") or ""
    if not website:
        score += 5
    elif len(website) > 0:
        score += 2

    return min(score, 25)

def _score_owner_exit(c: dict) -> float:
    score = 0.0
    # Founding officer still present (10 pts)
    if c.get("founding_officer_still_present"):
        score += 10
    elif c.get("incorporation_date"):
        score += 4

    # No management succession (5 pts)
    officer_count = c.get("officer_count") or 1
    if officer_count <= 2:
        score += 5
    elif officer_count <= 4:
        score += 2

    # Owner email is owner@ style (3 pts) — key-man signal
    email = (c.get("owner_email") or "").lower()
    if any(kw in email for kw in ["owner", "founder", "info", "admin"]):
        score += 3
    elif email:
        score += 1

    # Business age > 20 yrs bonus (7 pts)
    founded = c.get("founded_year")
    if founded and (CURRENT_YEAR - founded) >= 20:
        score += 7
    elif founded and (CURRENT_YEAR - founded) >= 15:
        score += 4

    return min(score, 25)

def _score_market(c: dict) -> float:
    score = 0.0
    # Fragmented industry (6 pts)
    _, is_fragmented, _ = get_industry_profile(c.get("naics_code"))
    score += 6 if is_fragmented else 2

    # Strong local brand (4 pts)
    rating = c.get("google_rating") or 0
    reviews = c.get("google_review_count") or 0
    if rating >= 4.0 and reviews >= 100:
        score += 4
    elif rating >= 4.0 and reviews >= 50:
        score += 2

    return min(score, 10)

def _score_outreach(c: dict) -> float:
    score = 0.0
    # Outreach priority (10 pts) - Just checking if we have contact info basically
    email = c.get("owner_email") or ""
    phone = c.get("phone") or ""
    if email and phone:
        score += 10
    elif email:
        score += 7
    elif phone:
        score += 4
    else:
        score += 1
    return score

def _classify_tier(total_score: float) -> str:
    if total_score >= 75:
        return "Tier 1"
    elif total_score >= 55:
        return "Tier 2"
    elif total_score >= 35:
        return "Tier 3"
    return "No Fit"
