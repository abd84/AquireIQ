import asyncio
from app.services.discovery.google_places import search_businesses
from app.api.routes.search import _enrich_and_score

async def main():
    print("Testing wider search (e.g. established businesses)...")
    try:
        raw_list = await search_businesses("Established accounting firm", "Dallas", "TX", max_results=5)
        for r in raw_list:
            company = await _enrich_and_score(r, "Dallas", "TX", min_age=0)
            if company:
                print(f"\n--- {company.name} ---")
                print(f"Score: {company.acquisition_score} ({company.score_tier})")
                if company.score_tier in ("Tier 1", "Tier 2"):
                    print("Gemini generated Explanation:", company.score_explanation)
                    print("Gemini generated Subject:", company.outreach_subject)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
