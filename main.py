"""
Influqa API Demo – Main Application
=====================================
A demonstration of the Influqa influencer marketing platform API.
Run with:  uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, influencers, campaigns, analytics

app = FastAPI(
    title="Influqa API Demo",
    description=(
        "## Influqa Influencer Marketing Platform – API Demo\n\n"
        "This demo showcases the core capabilities of the Influqa API:\n\n"
        "- **Authentication** – API key validation\n"
        "- **Influencer Discovery** – Search 50,000+ verified creators by niche, "
        "platform, follower count, engagement rate, and more\n"
        "- **Campaign Management** – Create and manage influencer marketing campaigns\n"
        "- **Analytics** – Measure campaign performance, ROI, and influencer metrics\n\n"
        "### Demo API Keys\n"
        "Use one of the following keys in the `X-API-Key` header:\n\n"
        "| Key | Role | Description |\n"
        "|-----|------|-------------|\n"
        "| `demo_key_brand` | Brand | Access as a brand running campaigns |\n"
        "| `demo_key_agency` | Agency | Access as a marketing agency |\n\n"
        "### Getting Started\n"
        "1. Click **Authorize** above and enter a demo API key.\n"
        "2. Try the **GET /influencers** endpoint to search for creators.\n"
        "3. Use **POST /campaigns** to create a campaign.\n"
        "4. Check **GET /analytics/overview** for performance metrics.\n"
    ),
    version="1.0.0",
    contact={
        "name": "Influqa",
        "url": "https://www.influqa.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(influencers.router)
app.include_router(campaigns.router)
app.include_router(analytics.router)


@app.get("/", include_in_schema=False)
def root():
    return {
        "name": "Influqa API Demo",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "demo_api_keys": ["demo_key_brand", "demo_key_agency"],
    }


@app.get("/health", tags=["Health"], summary="Health Check")
def health_check():
    """Returns the current health status of the API."""
    return {"status": "ok", "service": "influqa-api-demo"}
