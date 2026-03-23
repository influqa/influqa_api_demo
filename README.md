# Influqa API Demo

A demonstration of the **[Influqa](https://www.influqa.com)** Influencer Marketing Platform API with **Role-Based Access Control (RBAC)**. This demo showcases how different user types have access to different resources.

## 🎯 Key Features

### Role-Based Access Control

The API implements strict access control based on user type:

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

### Access Rules

1. **Agency users** can only see:
   - Influencers they manage
   - Offers received by their managed influencers
   - Campaigns their influencers are hired in

2. **Brand/Business users** can only see:
   - Their own campaigns
   - Influencers they work with (hired in their campaigns)
   - Offers they sent

3. **Influencer/Creator users** can only see:
   - Their own profile
   - Campaigns they're hired in
   - Offers they received

4. **Nonprofit/Education users** have limited access:
   - Only their own campaigns
   - No influencer discovery

## 📋 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/verify` | Verify API key and get access summary |
| GET | `/auth/demo-keys` | List all demo API keys |

### Influencer Discovery
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/influencers` | List influencers (filtered by access) |
| GET | `/influencers/{id}` | Get influencer details |
| GET | `/influencers/{id}/offers` | Get influencer's offers |

### Campaign Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/campaigns` | List campaigns (filtered by access) |
| GET | `/campaigns/{id}` | Get campaign details |
| POST | `/campaigns` | Create new campaign |
| PATCH | `/campaigns/{id}/status` | Update campaign status |
| DELETE | `/campaigns/{id}` | Delete campaign |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/overview` | Get overview statistics |
| GET | `/analytics/campaigns/{id}` | Get campaign analytics |
| GET | `/analytics/influencers/{id}` | Get influencer analytics |

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/influqa/influqa_api_demo.git
cd influqa_api_demo
pip install -r requirements.txt
```

### 2. Run the Server

```bash
uvicorn main:app --reload
```

### 3. Explore the API

Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

## 🔑 Demo API Keys

Use these keys in the `X-API-Key` header:

| API Key | User Type | Access Level |
|---------|-----------|--------------|
| `demo_key_admin` | admin | Full platform access - all influencers, campaigns, offers |
| `demo_key_brand` | brand | Own campaigns + partnered influencers |
| `demo_key_agency` | agency | 3 managed influencers + their offers |
| `demo_key_influencer` | influencer | Own profile (Emma) + received offers |
| `demo_key_creator` | creator | Own profile (Alex) + campaigns |
| `demo_key_business` | business | Own campaigns + partnered influencers |
| `demo_key_nonprofit` | nonprofit | Own campaign only |

## 📝 Example Requests

### Verify API Key

```bash
curl -X GET "http://localhost:8000/auth/verify" \
  -H "X-API-Key: demo_key_agency"
```

Response:
```json
{
  "success": true,
  "message": "API key is valid",
  "user": {
    "user_id": "user_agency_001",
    "user_type": "agency",
    "company_name": "Creative Talent Agency"
  },
  "access_summary": {
    "accessible_influencers": 3,
    "accessible_campaigns": 2,
    "accessible_offers": 4,
    "permissions": ["read:managed_influencers", "read:related_campaigns", ...]
  }
}
```

### List Influencers (Agency)

```bash
curl -X GET "http://localhost:8000/influencers" \
  -H "X-API-Key: demo_key_agency"
```

Returns only the 3 influencers managed by this agency.

### List Campaigns (Brand)

```bash
curl -X GET "http://localhost:8000/campaigns" \
  -H "X-API-Key: demo_key_brand"
```

Returns only campaigns owned by this brand.

### Access Denied Example

```bash
curl -X GET "http://localhost:8000/influencers/inf_003" \
  -H "X-API-Key: demo_key_agency"
```

Response (403 Forbidden):
```json
{
  "detail": "Access denied. You don't have permission to view influencer inf_003."
}
```

## 🏗️ Project Structure

```
influqa_api_demo/
├── main.py              # FastAPI application entry point
├── auth.py              # Authentication utilities
├── models.py            # Pydantic models
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── data/
│   ├── __init__.py
│   └── sample_data.py   # Mock data + access control functions
├── routers/
│   ├── __init__.py
│   ├── auth.py          # Authentication endpoints
│   ├── influencers.py   # Influencer discovery endpoints
│   ├── campaigns.py     # Campaign management endpoints
│   └── analytics.py     # Analytics endpoints
├── examples/
│   ├── basic_usage.py   # Basic API usage examples
│   └── campaign_workflow.py  # Full campaign workflow
└── tests/
    └── test_api.py      # Test suite
```

## 🔒 Access Control Implementation

The access control is implemented through helper functions in `data/sample_data.py`:

```python
def get_user_accessible_influencer_ids(user: dict) -> list:
    """
    Get list of influencer IDs the user can access.
    
    - admin: All influencers
    - agency: Influencers they manage
    - brand/business: Influencers they work with
    - influencer/creator: Only themselves
    - nonprofit/education: Empty (no access)
    """
```

Each endpoint uses these functions to filter results:

```python
@router.get("/influencers")
async def list_influencers(user: dict = get_current_user):
    accessible_ids = get_user_accessible_influencer_ids(user)
    influencers = [inf for inf in SAMPLE_INFLUENCERS if inf["id"] in accessible_ids]
    return {"data": influencers}
```

## 🧪 Testing

```bash
# Run tests
pytest tests/test_api.py -v

# Test with different user types
pytest tests/test_api.py -v -k "test_agency_access"
```

## 📚 Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🤝 Integration

To integrate with the real Influqa API:

1. Replace demo data with real API calls
2. Update authentication to use real API keys
3. Implement proper database queries
4. Add rate limiting and caching

## 📄 License

MIT License - See LICENSE file for details.

---

Built with ❤️ by the [Influqa](https://www.influqa.com) team