import json


def score_explanation_prompt(company: dict, score_total: float, score_tier: str, score_breakdown: dict) -> str:
    return f"""Analyze this pre-market SMB acquisition target.

Company: {company.get('name')}
Industry: {company.get('industry_description')}
Founded: {company.get('founded_year')}
Location: {company.get('hq_city')}, {company.get('hq_state')}
Employees: {company.get('employee_count_low')} - {company.get('employee_count_high')}
Revenue Estimate: ${company.get('revenue_estimate_low')} - ${company.get('revenue_estimate_high')}

Succession Readiness Score: {score_total}/100 ({score_tier})
Score Breakdown:
{json.dumps(score_breakdown, indent=2)}

Provide a 2-3 paragraph explanation of why this company received this score. Focus on succession readiness, owner exit signals (like business age), and financial/operational fit. Be analytical and professional."""


def outreach_email_prompt(company: dict) -> str:
    return f"""You are an M&A partner at a private equity firm reaching out to a business owner.
Write a 3-paragraph cold email to the owner. Do not sound salesy.
Frame it as a partnership/succession discussion.

Owner Name: {company.get('owner_name') or 'Business Owner'}
Company: {company.get('name')}
Industry: {company.get('industry_description')}
Founded: {company.get('founded_year')}
Location: {company.get('hq_city')}

Return ONLY valid JSON with exactly two keys: "subject" and "body". The body should have proper line breaks and be ready to send."""
