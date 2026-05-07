"""
Tests for AI generation layer (Gemini client + prompts).
All Gemini API calls are mocked — no real network calls.
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.services.scoring.engine import ScoreResult


def _make_score(total=72.0, tier="Tier 2"):
    return ScoreResult(
        total=total,
        tier=tier,
        breakdown={
            "financial_fit": 22.0,
            "operational_profile": 18.0,
            "owner_exit_signals": 20.0,
            "market_positioning": 6.0,
            "outreach_priority": 6.0,
        }
    )


def _base_company():
    return {
        "name": "Acme HVAC Services",
        "industry_description": "HVAC contractor",
        "founded_year": 1998,
        "hq_city": "Tulsa",
        "hq_state": "OK",
        "employee_count_low": 20,
        "employee_count_high": 40,
        "revenue_estimate_low": 2_000_000,
        "revenue_estimate_high": 8_000_000,
        "owner_name": "John Smith",
    }


# ── Prompts ───────────────────────────────────────────────────────────────────

def test_score_explanation_prompt_contains_company_name():
    from app.services.ai.prompts import score_explanation_prompt
    prompt = score_explanation_prompt(_base_company(), 72.0, "Tier 2", {"financial_fit": 22})
    assert "Acme HVAC Services" in prompt

def test_score_explanation_prompt_contains_score():
    from app.services.ai.prompts import score_explanation_prompt
    prompt = score_explanation_prompt(_base_company(), 72.0, "Tier 2", {"financial_fit": 22})
    assert "72.0" in prompt
    assert "Tier 2" in prompt

def test_outreach_email_prompt_contains_owner_name():
    from app.services.ai.prompts import outreach_email_prompt
    prompt = outreach_email_prompt(_base_company())
    assert "John Smith" in prompt

def test_outreach_email_prompt_requests_json():
    from app.services.ai.prompts import outreach_email_prompt
    prompt = outreach_email_prompt(_base_company())
    assert "JSON" in prompt
    assert "subject" in prompt
    assert "body" in prompt

def test_outreach_prompt_uses_fallback_owner_name():
    from app.services.ai.prompts import outreach_email_prompt
    c = {**_base_company(), "owner_name": None}
    prompt = outreach_email_prompt(c)
    assert "Business Owner" in prompt


# ── Gemini client — score explanation ────────────────────────────────────────

@pytest.mark.asyncio
async def test_generate_score_explanation_returns_string():
    from app.services.ai import gemini_client

    mock_response = MagicMock()
    mock_response.text = "This company shows strong succession readiness signals."

    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with patch.object(gemini_client, "_get_model", return_value=mock_model):
        result = await gemini_client.generate_score_explanation(_base_company(), _make_score())

    assert isinstance(result, str)
    assert "succession" in result.lower()


@pytest.mark.asyncio
async def test_generate_score_explanation_passes_breakdown():
    from app.services.ai import gemini_client

    mock_response = MagicMock()
    mock_response.text = "Explanation text."
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    captured_prompt = {}

    def capture(prompt):
        captured_prompt["value"] = prompt
        return mock_response

    mock_model.generate_content.side_effect = capture

    with patch.object(gemini_client, "_get_model", return_value=mock_model):
        await gemini_client.generate_score_explanation(_base_company(), _make_score())

    assert "financial_fit" in captured_prompt["value"]


# ── Gemini client — outreach email ───────────────────────────────────────────

@pytest.mark.asyncio
async def test_generate_outreach_email_returns_dict_for_tier1():
    from app.services.ai import gemini_client
    import json

    payload = {"subject": "Partnership Discussion", "body": "Dear John, ..."}
    mock_response = MagicMock()
    mock_response.text = json.dumps(payload)
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with patch.object(gemini_client, "_get_model", return_value=mock_model):
        result = await gemini_client.generate_outreach_email(_base_company(), _make_score(total=80, tier="Tier 1"))

    assert result["subject"] == "Partnership Discussion"
    assert "John" in result["body"]


@pytest.mark.asyncio
async def test_generate_outreach_email_skips_tier3():
    from app.services.ai import gemini_client

    with patch.object(gemini_client, "_get_model") as mock_get_model:
        result = await gemini_client.generate_outreach_email(_base_company(), _make_score(total=40, tier="Tier 3"))

    mock_get_model.assert_not_called()
    assert result == {"subject": "", "body": ""}


@pytest.mark.asyncio
async def test_generate_outreach_email_skips_no_fit():
    from app.services.ai import gemini_client

    with patch.object(gemini_client, "_get_model") as mock_get_model:
        result = await gemini_client.generate_outreach_email(_base_company(), _make_score(total=20, tier="No Fit"))

    mock_get_model.assert_not_called()
    assert result == {"subject": "", "body": ""}


@pytest.mark.asyncio
async def test_generate_outreach_email_handles_invalid_json():
    from app.services.ai import gemini_client

    mock_response = MagicMock()
    mock_response.text = "Sorry, here is the email body without JSON wrapper."
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response

    with patch.object(gemini_client, "_get_model", return_value=mock_model):
        result = await gemini_client.generate_outreach_email(_base_company(), _make_score(total=80, tier="Tier 1"))

    assert result["subject"] == "Private Equity Inquiry"
    assert result["body"] == mock_response.text
