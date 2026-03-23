"""
Authentication endpoints.

Validates API key and returns user info including access level.
"""

from fastapi import APIRouter, HTTPException
from auth import get_current_user
from data.sample_data import (
    get_user_accessible_campaign_ids, 
    get_user_accessible_influencer_ids,
    get_user_accessible_offer_ids,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/verify")
async def verify_api_key(user: dict = get_current_user):
    """
    Verify your API key and get user information.
    
    **Returns:**
    - User ID and type
    - VIP tier
    - Access level summary
    - Number of accessible resources
    
    **Demo API Keys:**
    - `demo_key_influencer` - Influencer account (SVIP)
    - `demo_key_business` - Business account (GVIP)
    - `demo_key_agency` - Agency account (GVIP)
    - `demo_key_nonprofit` - Nonprofit account (SVIP)
    - `demo_key_education` - Education account (Basic)
    """
    # Get access summary
    accessible_influencers = get_user_accessible_influencer_ids(user)
    accessible_campaigns = get_user_accessible_campaign_ids(user)
    accessible_offers = get_user_accessible_offer_ids(user)
    
    return {
        "success": True,
        "message": "API key is valid",
        "user": {
            "user_id": user["user_id"],
            "user_type": user["user_type"],
            "vip_tier": user.get("vip_tier", "basic"),
            "email": user.get("email"),
            "company_name": user.get("company_name"),
            "organization_name": user.get("organization_name"),
            "username": user.get("username"),
        },
        "access_summary": {
            "user_type": user["user_type"],
            "accessible_influencers": len(accessible_influencers),
            "accessible_campaigns": len(accessible_campaigns),
            "accessible_offers": len(accessible_offers),
            "permissions": get_permissions_for_user_type(user["user_type"]),
        },
    }


def get_permissions_for_user_type(user_type: str) -> list:
    """Get list of permissions for a user type."""
    permissions = {
        "business": [
            "read:partnered_influencers",
            "read:own_campaigns",
            "read:own_offers",
            "read:own_analytics",
            "create:campaigns",
            "update:own_campaigns",
            "delete:own_campaigns",
            "send:offers",
        ],
        "agency": [
            "read:managed_influencers",
            "read:related_campaigns",
            "read:related_offers",
            "read:related_analytics",
            "manage:influencer_profiles",
        ],
        "influencer": [
            "read:own_profile",
            "read:own_campaigns",
            "read:own_offers",
            "read:own_analytics",
            "update:own_profile",
            "accept:offers",
            "decline:offers",
        ],
        "nonprofit": [
            "read:own_campaigns",
            "read:own_offers",
            "read:own_analytics",
            "create:campaigns",
            "update:own_campaigns",
            "delete:own_campaigns",
            "send:offers",
        ],
        "education": [
            "read:own_campaigns",
            "read:own_offers",
            "read:own_analytics",
            "create:campaigns",
            "update:own_campaigns",
            "delete:own_campaigns",
            "send:offers",
        ],
    }
    return permissions.get(user_type, [])


@router.get("/demo-keys")
async def list_demo_keys():
    """
    List all available demo API keys for testing.
    
    Use these keys in the X-API-Key header to test different user roles.
    """
    return {
        "success": True,
        "message": "Use these API keys in the X-API-Key header",
        "demo_keys": [
            {
                "api_key": "demo_key_influencer",
                "user_type": "influencer",
                "vip_tier": "svip",
                "description": "Influencer account - creator profile",
                "access_level": "Own profile + campaigns hired for + offers received",
            },
            {
                "api_key": "demo_key_business",
                "user_type": "business",
                "vip_tier": "gvip",
                "description": "Business account - create campaigns",
                "access_level": "Own campaigns + partnered influencers + offers sent",
            },
            {
                "api_key": "demo_key_agency",
                "user_type": "agency",
                "vip_tier": "gvip",
                "description": "Agency account - manages influencers",
                "access_level": "Managed influencers (3) + their campaigns + offers received by them",
            },
            {
                "api_key": "demo_key_nonprofit",
                "user_type": "nonprofit",
                "vip_tier": "svip",
                "description": "Nonprofit organization account",
                "access_level": "Own campaigns only",
            },
            {
                "api_key": "demo_key_education",
                "user_type": "education",
                "vip_tier": "basic",
                "description": "Education organization account",
                "access_level": "Own campaigns only",
            },
        ],
    }