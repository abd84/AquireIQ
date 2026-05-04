from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import search, companies, enrichment, outreach

app = FastAPI(title="AcquireIQ API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://*.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional placeholder until routes are actually created
try:
    app.include_router(search.router, prefix="/api", tags=["search"])
    app.include_router(companies.router, prefix="/api", tags=["companies"])
    app.include_router(enrichment.router, prefix="/api", tags=["enrichment"])
    app.include_router(outreach.router, prefix="/api", tags=["outreach"])
except AttributeError:
    pass # Wait until we create them

@app.get("/health")
async def health():
    return {"status": "ok"}
