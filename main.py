"""
Influqa API Demo - FastAPI Application

A demonstration of the Influqa Influencer Marketing Platform API with role-based access control.
Based on pricing plans from https://www.influqa.com/pricing

User Types:
- Influencer: Can see own profile, offers received, campaigns hired for
- Business: Can create campaigns, see partnered influencers, send offers
- Nonprofit: Can create campaigns, limited access
- Agency: Manages influencers, sees their campaigns and offers
- Education: Can create campaigns, limited access

VIP Tiers: Basic (FREE), SVIP ($4.99/mo), GVIP ($19.99/mo)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, influencers, campaigns, analytics

app = FastAPI(
    title="Influqa API Demo",
    description="""
## Influqa Influencer Marketing Platform API

This demo showcases the Influqa API with **role-based access control**. Different user types 
have access to different resources based on their subscription plan.

### 👥 User Types & Access Levels

| User Type | Influencers | Campaigns | Offers | Analytics |
|-----------|-------------|-----------|--------|-----------|
| **Influencer** | Own only | Hired in only | Received only | Own performance |
| **Business** | Partnered only | Own only | Sent only | Own campaigns |
| **Agency** | Managed only | Related | Received by managed | Related |
| **Nonprofit** | None | Own only | Sent only | Own campaigns |
| **Education** | None | Own only | Sent only | Own campaigns |

### 💎 VIP Tiers

| Tier | Price | Features |
|------|-------|----------|
| **Basic** | FREE | Limited API access |
| **SVIP** | $4.99/mo | Enhanced access |
| **GVIP** | $19.99/mo | Full access |

### 🔑 Demo API Keys

Use these keys in the `X-API-Key` header:

| API Key | User Type | VIP Tier |
|---------|-----------|----------|
| `demo_key_influencer` | Influencer | SVIP |
| `demo_key_business` | Business | GVIP |
| `demo_key_agency` | Agency | GVIP |
| `demo_key_nonprofit` | Nonprofit | SVIP |
| `demo_key_education` | Education | Basic |

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
        "pricing": "https://www.influqa.com/pricing",
        "docs": "/docs",
        "redoc": "/redoc",
        "user_types": {
            "influencer": "Creator profile - receive offers, join campaigns",
            "business": "Create campaigns, work with influencers",
            "agency": "Manage multiple influencers",
            "nonprofit": "Organization campaigns (limited)",
            "education": "Educational campaigns (limited)",
        },
        "vip_tiers": {
            "basic": "FREE - Limited access",
            "svip": "$4.99/mo - Enhanced access",
            "gvip": "$19.99/mo - Full access",
        },
        "demo_keys": {
            "influencer": "demo_key_influencer",
            "business": "demo_key_business",
            "agency": "demo_key_agency",
            "nonprofit": "demo_key_nonprofit",
            "education": "demo_key_education",
        },
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0.0",
    }