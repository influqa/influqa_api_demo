"""
Influqa API Demo - FastAPI Application

A demonstration of the Influqa Influencer Marketing Platform API with role-based access control.

User Types and Access:
- admin: Full access to all resources
- brand: Own campaigns + partnered influencers + offers sent
- agency: Managed influencers + their campaigns + offers received by them
- influencer/creator: Own profile + campaigns hired for + offers received
- business: Own campaigns + partnered influencers + offers sent
- nonprofit/education: Own campaigns only (limited access)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, influencers, campaigns, analytics

app = FastAPI(
    title="Influqa API Demo",
    description="""
## Influqa Influencer Marketing Platform API

This demo showcases the Influqa API with **role-based access control**. Different user types 
have access to different resources based on their role.

### 🔐 User Types & Access Levels

| User Type | Influencers | Campaigns | Offers | Analytics |
|-----------|-------------|-----------|--------|-----------|
| **admin** | All | All | All | All |
| **brand** | Partnered only | Own only | Sent only | Own campaigns |
| **agency** | Managed only | Related | Received by managed | Related |
| **influencer** | Own only | Hired in only | Received only | Own performance |
| **creator** | Own only | Hired in only | Received only | Own performance |
| **business** | Partnered only | Own only | Sent only | Own campaigns |
| **nonprofit** | None | Own only | Sent only | Own campaigns |
| **education** | None | Own only | Sent only | Own campaigns |

### 📝 Demo API Keys

Use these keys in the `X-API-Key` header:

| API Key | User Type | Description |
|---------|-----------|-------------|
| `demo_key_admin` | admin | Full platform access |
| `demo_key_brand` | brand | Brand account with campaigns |
| `demo_key_agency` | agency | Agency managing 3 influencers |
| `demo_key_influencer` | influencer | Influencer profile (Emma) |
| `demo_key_creator` | creator | Creator profile (Alex) |
| `demo_key_business` | business | Business account |
| `demo_key_nonprofit` | nonprofit | Nonprofit organization |

### 🚀 Quick Start

1. **Verify your API key:** `GET /auth/verify`
2. **List available demo keys:** `GET /auth/demo-keys`
3. **Explore endpoints based on your access level**

### 📖 Endpoints

- **Authentication:** `/auth/*` - API key verification
- **Influencers:** `/influencers/*` - Discover and view influencers
- **Campaigns:** `/campaigns/*` - Manage campaigns
- **Analytics:** `/analytics/*` - Performance metrics
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(influencers.router)
app.include_router(campaigns.router)
app.include_router(analytics.router)


@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with quick links."""
    return {
        "name": "Influqa API Demo",
        "version": "2.0.0",
        "description": "Influencer Marketing Platform API with Role-Based Access Control",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "auth": {
                "verify": "/auth/verify",
                "demo_keys": "/auth/demo-keys",
            },
            "influencers": {
                "list": "/influencers",
                "get": "/influencers/{influencer_id}",
                "offers": "/influencers/{influencer_id}/offers",
            },
            "campaigns": {
                "list": "/campaigns",
                "get": "/campaigns/{campaign_id}",
                "create": "/campaigns (POST)",
                "update_status": "/campaigns/{campaign_id}/status (PATCH)",
                "delete": "/campaigns/{campaign_id} (DELETE)",
            },
            "analytics": {
                "overview": "/analytics/overview",
                "campaign": "/analytics/campaigns/{campaign_id}",
                "influencer": "/analytics/influencers/{influencer_id}",
            },
        },
        "demo_keys": {
            "admin": "demo_key_admin",
            "brand": "demo_key_brand",
            "agency": "demo_key_agency",
            "influencer": "demo_key_influencer",
            "creator": "demo_key_creator",
            "business": "demo_key_business",
            "nonprofit": "demo_key_nonprofit",
        },
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0.0",
    }