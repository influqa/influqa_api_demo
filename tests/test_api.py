"""
Tests for the Influqa API Demo.
"""

import pytest
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)
BRAND_HEADERS = {"X-API-Key": "demo_key_brand"}
AGENCY_HEADERS = {"X-API-Key": "demo_key_agency"}
INVALID_HEADERS = {"X-API-Key": "invalid_key"}


# ── Health & Root ─────────────────────────────────────────────────────────────

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Influqa API Demo"
    assert "docs" in data


# ── Authentication ────────────────────────────────────────────────────────────

def test_verify_valid_brand_key():
    response = client.get("/auth/verify", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "brand"
    assert data["user_id"] == "brand_001"


def test_verify_valid_agency_key():
    response = client.get("/auth/verify", headers=AGENCY_HEADERS)
    assert response.status_code == 200
    assert response.json()["role"] == "agency"


def test_verify_invalid_key():
    response = client.get("/auth/verify", headers=INVALID_HEADERS)
    assert response.status_code == 401


def test_missing_api_key():
    response = client.get("/auth/verify")
    assert response.status_code == 422


# ── Influencers ───────────────────────────────────────────────────────────────

def test_list_influencers():
    response = client.get("/influencers", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "influencers" in data
    assert data["total"] >= 1
    assert data["page"] == 1


def test_filter_by_platform():
    response = client.get("/influencers?platform=instagram", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    for inf in data["influencers"]:
        assert inf["platform"] == "instagram"


def test_filter_by_niche():
    response = client.get("/influencers?niche=fitness", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    for inf in data["influencers"]:
        assert inf["niche"] == "fitness"


def test_filter_verified_only():
    response = client.get("/influencers?verified_only=true", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    for inf in data["influencers"]:
        assert inf["verified"] is True


def test_filter_min_followers():
    response = client.get("/influencers?min_followers=400000", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    for inf in data["influencers"]:
        assert inf["follower_count"] >= 400000


def test_filter_tags():
    response = client.get("/influencers?tags=travel", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    for inf in data["influencers"]:
        assert "travel" in [t.lower() for t in inf["tags"]]


def test_get_influencer_by_id():
    response = client.get("/influencers/inf_001", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "inf_001"
    assert data["username"] == "lifestyle_with_emma"


def test_get_influencer_not_found():
    response = client.get("/influencers/inf_999", headers=BRAND_HEADERS)
    assert response.status_code == 404


def test_influencers_require_auth():
    response = client.get("/influencers")
    assert response.status_code == 422


# ── Campaigns ─────────────────────────────────────────────────────────────────

CAMPAIGN_PAYLOAD = {
    "title": "Test Campaign for Unit Tests",
    "description": "A test campaign created during unit testing",
    "niche": "technology",
    "platforms": ["instagram"],
    "budget": 5000,
    "currency": "USD",
    "influencer_requirements": {
        "min_followers": 50000,
        "min_engagement_rate": 3.0,
        "required_niches": ["technology"],
        "preferred_locations": ["US"],
    },
    "deliverables": [{"type": "feed_post", "count": 1}],
    "start_date": "2025-08-01",
    "end_date": "2025-08-31",
}


def test_list_campaigns():
    response = client.get("/campaigns", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "campaigns" in data
    assert isinstance(data["total"], int)


def test_create_campaign():
    response = client.post("/campaigns", headers=BRAND_HEADERS, json=CAMPAIGN_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == CAMPAIGN_PAYLOAD["title"]
    assert data["status"] == "draft"
    assert data["brand_id"] == "brand_001"


def test_get_campaign():
    # First create one
    create_resp = client.post("/campaigns", headers=BRAND_HEADERS, json=CAMPAIGN_PAYLOAD)
    campaign_id = create_resp.json()["id"]
    response = client.get(f"/campaigns/{campaign_id}", headers=BRAND_HEADERS)
    assert response.status_code == 200
    assert response.json()["id"] == campaign_id


def test_get_campaign_not_found():
    response = client.get("/campaigns/camp_999", headers=BRAND_HEADERS)
    assert response.status_code == 404


def test_update_campaign_status():
    create_resp = client.post("/campaigns", headers=BRAND_HEADERS, json=CAMPAIGN_PAYLOAD)
    campaign_id = create_resp.json()["id"]
    response = client.patch(
        f"/campaigns/{campaign_id}/status?status=active", headers=BRAND_HEADERS
    )
    assert response.status_code == 200
    assert response.json()["status"] == "active"


def test_update_campaign_invalid_status():
    create_resp = client.post("/campaigns", headers=BRAND_HEADERS, json=CAMPAIGN_PAYLOAD)
    campaign_id = create_resp.json()["id"]
    response = client.patch(
        f"/campaigns/{campaign_id}/status?status=invalid", headers=BRAND_HEADERS
    )
    assert response.status_code == 400


def test_delete_draft_campaign():
    create_resp = client.post("/campaigns", headers=BRAND_HEADERS, json=CAMPAIGN_PAYLOAD)
    campaign_id = create_resp.json()["id"]
    response = client.delete(f"/campaigns/{campaign_id}", headers=BRAND_HEADERS)
    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()


def test_delete_active_campaign_fails():
    create_resp = client.post("/campaigns", headers=BRAND_HEADERS, json=CAMPAIGN_PAYLOAD)
    campaign_id = create_resp.json()["id"]
    client.patch(f"/campaigns/{campaign_id}/status?status=active", headers=BRAND_HEADERS)
    response = client.delete(f"/campaigns/{campaign_id}", headers=BRAND_HEADERS)
    assert response.status_code == 400


def test_create_campaign_missing_fields():
    response = client.post("/campaigns", headers=BRAND_HEADERS, json={"title": "Oops"})
    assert response.status_code == 422


# ── Analytics ─────────────────────────────────────────────────────────────────

def test_get_campaign_analytics():
    response = client.get("/analytics/campaigns/camp_001", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["campaign_id"] == "camp_001"
    assert data["total_reach"] > 0
    assert data["roi"] > 0
    assert len(data["influencer_performance"]) > 0


def test_get_analytics_not_found():
    response = client.get("/analytics/campaigns/camp_999", headers=BRAND_HEADERS)
    assert response.status_code == 404


def test_get_overview():
    response = client.get("/analytics/overview", headers=BRAND_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "total_campaigns" in data
    assert "average_roi" in data
    assert data["brand_id"] == "brand_001"
