"""
Test suite for Influqa API Demo with role-based access control.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAuth:
    """Authentication tests."""
    
    def test_verify_admin_key(self):
        """Admin key should have full access."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "demo_key_admin"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["user"]["user_type"] == "admin"
        assert data["access_summary"]["accessible_influencers"] == 5  # All
    
    def test_verify_agency_key(self):
        """Agency key should have limited access."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "demo_key_agency"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["user_type"] == "agency"
        assert data["access_summary"]["accessible_influencers"] == 3  # Managed
    
    def test_verify_brand_key(self):
        """Brand key should have limited access."""
        response = client.get(
            "/auth/verify",
            headers={"X-API-Key": "demo_key_brand"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["user_type"] == "brand"
    
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
        assert len(data["demo_keys"]) == 7


class TestInfluencerAccess:
    """Influencer endpoint access control tests."""
    
    def test_admin_sees_all_influencers(self):
        """Admin should see all influencers."""
        response = client.get(
            "/influencers",
            headers={"X-API-Key": "demo_key_admin"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 5
        assert data["access_level"] == "full"
    
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
    
    def test_brand_sees_partnered_influencers(self):
        """Brand should see only partnered influencers."""
        response = client.get(
            "/influencers",
            headers={"X-API-Key": "demo_key_brand"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2  # Emma and Nina
    
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
    
    def test_admin_sees_all_campaigns(self):
        """Admin should see all campaigns."""
        response = client.get(
            "/campaigns",
            headers={"X-API-Key": "demo_key_admin"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 4
    
    def test_brand_sees_own_campaigns(self):
        """Brand should see only own campaigns."""
        response = client.get(
            "/campaigns",
            headers={"X-API-Key": "demo_key_brand"}
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
    
    def test_business_sees_own_campaigns(self):
        """Business should see own campaigns."""
        response = client.get(
            "/campaigns",
            headers={"X-API-Key": "demo_key_business"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 1
    
    def test_campaign_detail_access_control(self):
        """Campaign detail should respect access control."""
        # Admin can access any campaign
        response = client.get(
            "/campaigns/camp_001",
            headers={"X-API-Key": "demo_key_admin"}
        )
        assert response.status_code == 200
        
        # Non-owner brand cannot access
        response = client.get(
            "/campaigns/camp_003",  # Owned by business
            headers={"X-API-Key": "demo_key_brand"}
        )
        assert response.status_code == 403


class TestCampaignCreate:
    """Campaign creation access control tests."""
    
    def test_brand_can_create_campaign(self):
        """Brand should be able to create campaigns."""
        response = client.post(
            "/campaigns",
            headers={"X-API-Key": "demo_key_brand"},
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
            headers={"X-API-Key": "demo_key_brand"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data["data"]
    
    def test_campaign_analytics_access_control(self):
        """Campaign analytics should respect access control."""
        # Admin can access
        response = client.get(
            "/analytics/campaigns/camp_001",
            headers={"X-API-Key": "demo_key_admin"}
        )
        assert response.status_code == 200
        
        # Non-owner cannot access
        response = client.get(
            "/analytics/campaigns/camp_003",
            headers={"X-API-Key": "demo_key_brand"}
        )
        assert response.status_code == 403


class TestRootEndpoints:
    """Root endpoint tests."""
    
    def test_root(self):
        """Root endpoint should return API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Influqa API Demo"
        assert "demo_keys" in data
    
    def test_health(self):
        """Health endpoint should return healthy."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"