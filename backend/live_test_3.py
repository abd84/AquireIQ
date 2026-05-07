import asyncio
from app.services.discovery.google_places import search_businesses
from app.api.routes.search import _enrich_and_score

async def main():
    print("Testing for highest tier (Simulating High Score via forcing)...")
    try:
        raw_list = await search_businesses("Old HVAC contractor 1980", "Chicago", "IL", max_results=1)
        r = raw_list[0]
        # Force the score signals up
        r["founded_year"] = 1990
        r["google_review_count"] = 250
        r["google_rating"] = 4.8
        r["revenue_estimate_low"] = 4000000 
        r["employee_count_low"] = 30
        r["owner_email"] = "owner@hvac.com"
        r["owner_name"] = "John Smith"
        
        company = await _enrich_and_score(r, "Chicago", "IL", min_age=0)
        if company:
            print(f"\n--- {company.name} ---")
            print(f"Score: {company.acquisition_score} ({company.score_tier})")
            if company.score_tier in ("Tier 1", "Tier 2"):
                print(f"Explanation:\n{company.score_explanation}")
                print(f"\nEmail Subj: {company.outreach_subject}")
                print(f"Email Body:\n{company.outreach_body}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
