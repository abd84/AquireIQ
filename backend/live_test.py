import asyncio
from app.services.discovery.google_places import search_businesses
from app.api.routes.search import _enrich_and_score
import json

async def main():
    print("Testing Discovery (Google Places)...")
    try:
        raw_list = await search_businesses("Plumbing", "Tulsa", "OK", max_results=3)
        print(f"Found {len(raw_list)} places.")
        for r in raw_list:
            print("-", r["name"], r.get("website"))
        
        if raw_list:
            print("\nTesting Enrichment, Scoring, and Gemini AI on the first result...")
            company = await _enrich_and_score(raw_list[0], "Tulsa", "OK", min_age=5)
            if company:
                print(f"Success! Name: {company.name}")
                print(f"Score: {company.acquisition_score} ({company.score_tier})")
                print("Explanation: ", company.score_explanation)
                print("Email Subject: ", company.outreach_subject)
                print("Email Body:\n", company.outreach_body)
                print("Hunter Email: ", company.owner_email)
            else:
                print("Company was filtered out (e.g. by age filter).")
    except Exception as e:
        print(f"Error during live test: {e}")

if __name__ == "__main__":
    asyncio.run(main())
