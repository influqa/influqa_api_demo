"""
Test suite for Influqa API Demo with role-based access control.
User types from https://www.influqa.com/pricing:
- Influencer
- Business
- Agency
- Nonprofit
- Education
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAuth:
    """Authentication tests."""
    
    def test_verify_influencer_key(self):
        """Influencer key should have limited access."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "demo_key_influencer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["user_type"] == "influencer"
        assert data["user"]["vip_tier"] == "svip"
    
    def test_verify_business_key(self):
        """Business key should have limited access."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "demo_key_business"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["user_type"] == "business"
        assert data["user"]["vip_tier"] == "gvip"
    
    def test_verify_agency_key(self):
        """Agency key should have managed influencer access."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "demo_key_agency"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["user_type"] == "agency"
        assert data["access_summary"]["accessible_influencers"] == 3
    
    def test_verify_nonprofit_key(self):
        """Nonprofit key should have limited access."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "demo_key_nonprofit"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["user_type"] == "nonprofit"
    
    def test_verify_education_key(self):
        """Education key should have limited access."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "demo_key_education"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["user_type"] == "education"
        assert data["user"]["vip_tier"] == "basic"
    
    def test_invalid_key(self):
        """Invalid key should return 401."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "invalid_key"}
        )
        assert response.status_code == 401
    
    def test_missing_key(self):
        """Missing key should return 422."""
        response = client.get("/auth/verify")
        assert response.status_code == 422
    
    def test_demo_keys_endpoint(self):
        """Demo keys listing should work."""
        response = client.get("/auth/demo-keys")
        assert response.status_code == 200
        data = response.json()
        assert len(data["demo_keys"]) == 5


class TestInfluencerAccess:
    """Influencer endpoint access control tests."""
    
    def test_agency_sees_managed_influencers(self):
        """Agency should see only managed influencers."""
        response = client.get(
            "/influencers",
            headers={"X-API-Key": "demo_key_agency"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 3
        assert data["user_type"] == "agency"
    
    def test_business_sees_partnered_influencers(self):
        """Business should see only partnered influencers."""
        response = client.get(
            "/influencers",
            headers={"X-API-Key": "demo_key_business"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2  # Emma and Marcus
    
    def test_influencer_sees_own_profile(self):
        """Influencer should see only own profile."""
        response = client.get(
            "/influencers",
            headers={"X-API-Key": "demo_key_influencer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
    
    def test_nonprofit_sees_no_influencers(self):
        """Nonprofit should not see any influencers."""
        response = client.get(
            "/influencers",
            headers={"X-API-Key": "demo_key_nonprofit"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
    
    def test_education_sees_no_influencers(self):
        """Education should not see any influencers."""
        response = client.get(
            "/influencers",
            headers={"X-API-Key": "demo_key_education"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
    
    def test_agency_cannot_access_non_managed_influencer(self):
        """Agency should get 403 for non-managed influencer."""
        response = client.get(
            "/influencers/inf_003",  # Sophia - not managed by demo agency
            headers={"X-API-Key": "demo_key_agency"}
        )
        assert response.status_code == 403
    
    def test_agency_can_access_managed_influencer(self):
        """Agency should access managed influencer."""
        response = client.get(
            "/influencers/inf_001",  # Emma - managed by demo agency
            headers={"X-API-Key": "demo_key_agency"}
        )
        assert response.status_code == 200
    
    def test_influencer_cannot_access_other_influencer(self):
        """Influencer should get 403 for another influencer."""
        response = client.get(
            "/influencers/inf_002",  # Marcus
            headers={"X-API-Key": "demo_key_influencer"}  # Emma
        )
        assert response.status_code == 403


class TestCampaignAccess:
    """Campaign endpoint access control tests."""
    
    def test_business_sees_own_campaigns(self):
        """Business should see only own campaigns."""
        response = client.get(
            "/campaigns",
            headers={"X-API-Key": "demo_key_business"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2  # camp_001 and camp_002
    
    def test_agency_sees_related_campaigns(self):
        """Agency should see campaigns their influencers are in."""
        response = client.get(
            "/campaigns",
            headers={"X-API-Key": "demo_key_agency"}
        )
        assert response.status_code == 200
    
    def test_nonprofit_sees_own_campaigns(self):
        """Nonprofit should see own campaigns."""
        response = client.get(
            "/campaigns",
            headers={"X-API-Key": "demo_key_nonprofit"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
    
    def test_education_sees_own_campaigns(self):
        """Education should see own campaigns."""
        response = client.get(
            "/campaigns",
            headers={"X-API-Key": "demo_key_education"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
    
    def test_campaign_detail_access_control(self):
        """Campaign detail should respect access control."""
        # Non-owner business cannot access
        response = client.get(
            "/campaigns/camp_003",  # Owned by nonprofit
            headers={"X-API-Key": "demo_key_business"}
        )
        assert response.status_code == 403


class TestCampaignCreate:
    """Campaign creation access control tests."""
    
    def test_business_can_create_campaign(self):
        """Business should be able to create campaigns."""
        response = client.post(
            "/campaigns",
            headers={"X-API-Key": "demo_key_business"},
            json={
                "title": "Test Campaign",
                "description": "Test",
                "niche": "lifestyle",
                "platforms": ["instagram"],
                "budget": 5000,
                "influencer_requirements": {
                    "min_followers": 10000
                },
                "deliverables": [
                    {"type": "feed_post", "count": 1}
                ],
                "start_date": "2025-01-01",
                "end_date": "2025-01-31"
            }
        )
        assert response.status_code == 200
    
    def test_nonprofit_can_create_campaign(self):
        """Nonprofit should be able to create campaigns."""
        response = client.post(
            "/campaigns",
            headers={"X-API-Key": "demo_key_nonprofit"},
            json={
                "title": "Test Campaign",
                "description": "Test",
                "niche": "lifestyle",
                "platforms": ["instagram"],
                "budget": 5000,
                "influencer_requirements": {},
                "deliverables": [],
                "start_date": "2025-01-01",
                "end_date": "2025-01-31"
            }
        )
        assert response.status_code == 200
    
    def test_agency_cannot_create_campaign(self):
        """Agency should not be able to create campaigns."""
        response = client.post(
            "/campaigns",
            headers={"X-API-Key": "demo_key_agency"},
            json={
                "title": "Test Campaign",
                "description": "Test",
                "niche": "lifestyle",
                "platforms": ["instagram"],
                "budget": 5000,
                "influencer_requirements": {},
                "deliverables": [],
                "start_date": "2025-01-01",
                "end_date": "2025-01-31"
            }
        )
        assert response.status_code == 403
    
    def test_influencer_cannot_create_campaign(self):
        """Influencer should not be able to create campaigns."""
        response = client.post(
            "/campaigns",
            headers={"X-API-Key": "demo_key_influencer"},
            json={
                "title": "Test Campaign",
                "description": "Test",
                "niche": "lifestyle",
                "platforms": ["instagram"],
                "budget": 5000,
                "influencer_requirements": {},
                "deliverables": [],
                "start_date": "2025-01-01",
                "end_date": "2025-01-31"
            }
        )
        assert response.status_code == 403


class TestAnalytics:
    """Analytics endpoint tests."""
    
    def test_analytics_overview(self):
        """Analytics overview should work."""
        response = client.get(
            "/analytics/overview",
            headers={"X-API-Key": "demo_key_business"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data["data"]
    
    def test_campaign_analytics_access_control(self):
        """Campaign analytics should respect access control."""
        # Non-owner cannot access
        response = client.get(
            "/analytics/campaigns/camp_003",
            headers={"X-API-Key": "demo_key_business"}
        )
        assert response.status_code == 403
    
    def test_influencer_analytics_access_control(self):
        """Influencer analytics should respect access control."""
        # Influencer can access own analytics
        response = client.get(
            "/analytics/influencers/inf_001",
            headers={"X-API-Key": "demo_key_influencer"}
        )
        assert response.status_code == 200
        
        # Influencer cannot access other's analytics
        response = client.get(
            "/analytics/influencers/inf_002",
            headers={"X-API-Key": "demo_key_influencer"}
        )
        assert response.status_code == 403


class TestVIPTiers:
    """VIP tier tests."""
    
    def test_vip_tier_returned_in_auth(self):
        """VIP tier should be returned in auth response."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "demo_key_business"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "vip_tier" in data["user"]
        assert data["user"]["vip_tier"] == "gvip"
    
    def test_vip_tier_in_analytics(self):
        """VIP tier should be shown in analytics."""
        response = client.get(
            "/analytics/overview",
            headers={"X-API-Key": "demo_key_influencer"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "vip_tier" in data["data"]


class TestRootEndpoints:
    """Root endpoint tests."""
    
    def test_root(self):
        """Root endpoint should return API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Influqa API Demo"
        assert "demo_keys" in data
        assert "pricing" in data
    
    def test_health(self):
        """Health endpoint should return healthy."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"