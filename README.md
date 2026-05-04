# AcquireIQ

AcquireIQ is an AI-powered M&A Deal Sourcing tool that fully automates the discovery, enrichment, scoring, and outreach pipeline for identifying SMB acquisition targets.

## Architecture

* **Frontend**: Next.js 14 (App router), React, TailwindCSS, TypeScript.
* **Backend**: FastAPI, SQLAlchemy 2.0 (async), PostgreSQL.
* **Workers**: Celery, Redis (for background data enrichment).
* **Intelligence**: Gemini 1.5 Flash (for AI scoring analysis and email drafting).
* **Enrichment Tooling**: Google Places API, custom web scraping, OpenCorporates API, Hunter.io API.

## Requirements

* Docker & Docker Compose
* Node.js >= 20 (if running frontend locally)
* Python >= 3.12 (if running backend locally)
* API Keys (Google Places, Hunter.io, Gemini)

## Quickstart (Docker Compose)

1. Clone the repository anywhere.
2. In the root `acquireiq` directory, create a `.env` file (or just pass them into compose):

```bash
GOOGLE_PLACES_API_KEY=your_key
HUNTER_API_KEY=your_key
GEMINI_API_KEY=your_key
```

3. Spin up the entire stack:
```bash
docker-compose up --build -d
```

4. Navigate to `http://localhost:3000` to view the unified Dashboard. The FastAPI backend is running on `http://localhost:8000`. 
5. To execute database migrations successfully you need to run:
```bash
docker-compose exec backend alembic upgrade head
```

## Usage

1. Open `http://localhost:3000/search` and search for "Dental Practices" or similar criteria.
2. Google Places will find N records and they will be pushed into PostgreSQL. 
3. Background Celery workers will scrape web domains, lookup the company names in OpenCorporates, and trigger Hunter.io API for the executives.
4. Gemini will compile a Succession Readiness Score.
5. The UI on `http://localhost:3000/companies` will auto-refresh and display the statuses changing from `enriching` to `completed` and displaying their readiness score out of 100.
6. The `Outreach Queue` dashboard handles generating a sequence list to drop into Hubspot/Apollo.

## License

MIT
