# Influqa API Demo

A demonstration of the **[Influqa](https://www.influqa.com)** Influencer Marketing Platform API, built with [FastAPI](https://fastapi.tiangolo.com/). This project showcases how to interact with the Influqa platform to discover verified creators, manage campaigns, and analyse performance.

## Features

| Module | Endpoints | Description |
|--------|-----------|-------------|
| **Authentication** | `GET /auth/verify` | Validate your API key |
| **Influencer Discovery** | `GET /influencers`, `GET /influencers/{id}` | Search & filter 50,000+ verified creators |
| **Campaign Management** | `POST /campaigns`, `GET /campaigns`, `GET /campaigns/{id}`, `PATCH /campaigns/{id}/status`, `DELETE /campaigns/{id}` | Full campaign lifecycle |
| **Analytics** | `GET /analytics/campaigns/{id}`, `GET /analytics/overview` | Performance metrics & ROI |

## Prerequisites

- Python 3.10+

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/influqa/influqa_api_demo.git
cd influqa_api_demo
pip install -r requirements.txt
```

### 2. Start the Server

```bash
uvicorn main:app --reload
```

The API will be available at **http://localhost:8000**.

### 3. Explore the Interactive Docs

Open your browser and navigate to:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

All endpoints (except `/health`) require an `X-API-Key` header.

Two demo API keys are provided:

| API Key | Role | Description |
|---------|------|-------------|
| `demo_key_brand` | Brand | Access as a brand running campaigns |
| `demo_key_agency` | Agency | Access as a marketing agency |

**Example request:**
```bash
curl -H "X-API-Key: demo_key_brand" http://localhost:8000/auth/verify
```

## API Reference

### Influencer Discovery

**Search influencers** with rich filtering:

```bash
# Find verified Instagram lifestyle influencers with 100k+ followers
curl -H "X-API-Key: demo_key_brand" \
  "http://localhost:8000/influencers?platform=instagram&niche=lifestyle&min_followers=100000&verified_only=true"
```

Available filters: `niche`, `platform`, `min_followers`, `max_followers`, `min_engagement_rate`, `location`, `verified_only`, `tags`, `page`, `per_page`.

**Get a specific influencer:**
```bash
curl -H "X-API-Key: demo_key_brand" http://localhost:8000/influencers/inf_001
```

### Campaign Management

**Create a campaign:**
```bash
curl -X POST http://localhost:8000/campaigns \
  -H "X-API-Key: demo_key_brand" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Summer Fashion 2025",
    "description": "Promote our new summer collection targeting millennials",
    "niche": "fashion",
    "platforms": ["instagram", "tiktok"],
    "budget": 15000,
    "currency": "USD",
    "influencer_requirements": {
      "min_followers": 50000,
      "min_engagement_rate": 3.5,
      "required_niches": ["fashion", "lifestyle"],
      "preferred_locations": ["US", "UK"]
    },
    "deliverables": [
      {"type": "feed_post", "count": 2},
      {"type": "story", "count": 5}
    ],
    "start_date": "2025-07-01",
    "end_date": "2025-07-31"
  }'
```

**Activate a campaign:**
```bash
curl -X PATCH "http://localhost:8000/campaigns/{id}/status?status=active" \
  -H "X-API-Key: demo_key_brand"
```

### Analytics

**Campaign performance:**
```bash
curl -H "X-API-Key: demo_key_brand" http://localhost:8000/analytics/campaigns/camp_001
```

**Account overview:**
```bash
curl -H "X-API-Key: demo_key_brand" http://localhost:8000/analytics/overview
```

## Example Scripts

Two complete example scripts are included in the `examples/` directory:

```bash
# Make sure the server is running first
uvicorn main:app --reload &

# Basic usage: verify auth, search influencers, view profiles
python examples/basic_usage.py

# Full campaign workflow: create → find influencers → activate → analyse
python examples/campaign_workflow.py
```

## Running Tests

```bash
pytest tests/test_api.py -v
```

## Project Structure

```
influqa_api_demo/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic data models
├── auth.py              # API key authentication helper
├── requirements.txt     # Python dependencies
├── routers/
│   ├── auth.py          # Authentication endpoints
│   ├── influencers.py   # Influencer discovery endpoints
│   ├── campaigns.py     # Campaign management endpoints
│   └── analytics.py     # Analytics & reporting endpoints
├── data/
│   └── sample_data.py   # Mock influencer, campaign & analytics data
├── examples/
│   ├── basic_usage.py   # Basic API usage example
│   └── campaign_workflow.py  # End-to-end campaign workflow
└── tests/
    └── test_api.py      # Comprehensive API tests (27 tests)
```

## Sample Data

The demo includes pre-loaded sample data:

**Influencers (5 verified creators):**
- Emma Johnson – Instagram Lifestyle (285k followers, 4.7% engagement)
- Marcus Chen – YouTube Technology (512k followers, 6.2% engagement)
- Sophia Martinez – TikTok Food (1.2M followers, 8.9% engagement)
- Alex Thompson – Instagram Fitness (98k followers, 5.8% engagement)
- Nina Patel – Instagram Beauty (420k followers, 5.1% engagement)

**Campaigns (2 pre-loaded):**
- `camp_001` – Summer Fashion Collection (active)
- `camp_002` – Healthy Living App Launch (completed)

## License

MIT
