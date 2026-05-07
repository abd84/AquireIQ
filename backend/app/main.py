from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import search, companies, outreach
from app.database import engine, Base
# Import all models so Base.metadata knows about every table
import app.models.company  # noqa: F401
import app.models.outreach  # noqa: F401
import app.models.enrichment_job  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="AcquireIQ API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(companies.router, prefix="/api", tags=["companies"])
app.include_router(outreach.router, prefix="/api", tags=["outreach"])

@app.get("/health")
async def health():
    return {"status": "ok"}
