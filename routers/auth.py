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
    - Access level summary
    - Number of accessible resources
    
    **Demo API Keys:**
    - `demo_key_brand` - Brand account (campaigns + partnered influencers)
    - `demo_key_agency` - Agency account (managed influencers + their offers)
    - `demo_key_influencer` - Influencer account (own profile + received offers)
    - `demo_key_creator` - Creator account (own profile + campaigns)
    - `demo_key_business` - Business account (campaigns + partnered influencers)
    - `demo_key_nonprofit` - Nonprofit account (limited access)
    - `demo_key_admin` - Admin account (full access to all)
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
        "admin": [
            "read:all_influencers",
            "read:all_campaigns",
            "read:all_offers",
            "read:all_analytics",
            "create:campaigns",
            "update:campaigns",
            "delete:campaigns",
            "manage:users",
        ],
        "brand": [
            "read:own_influencers",
            "read:own_campaigns",
            "read:own_offers",
            "read:own_analytics",
            "create:campaigns",
            "update:own_campaigns",
            "delete:own_campaigns",
            "send:offers",
        ],
        "business": [
            "read:own_influencers",
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
        "creator": [
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
                "api_key": "demo_key_admin",
                "user_type": "admin",
                "description": "Full access to all resources",
                "access_level": "Full platform access - can see all influencers, campaigns, offers, and analytics",
            },
            {
                "api_key": "demo_key_brand",
                "user_type": "brand",
                "description": "Brand account - can create campaigns and work with influencers",
                "access_level": "Own campaigns + influencers they work with + offers sent",
            },
            {
                "api_key": "demo_key_agency",
                "user_type": "agency",
                "description": "Agency account - manages multiple influencers",
                "access_level": "Managed influencers (3) + their campaigns + offers received by them",
            },
            {
                "api_key": "demo_key_influencer",
                "user_type": "influencer",
                "description": "Influencer account - creator profile",
                "access_level": "Own profile + campaigns hired for + offers received",
            },
            {
                "api_key": "demo_key_creator",
                "user_type": "creator",
                "description": "Creator account - similar to influencer",
                "access_level": "Own profile + campaigns hired for + offers received",
            },
            {
                "api_key": "demo_key_business",
                "user_type": "business",
                "description": "Business account - similar to brand",
                "access_level": "Own campaigns + partnered influencers + offers sent",
            },
            {
                "api_key": "demo_key_nonprofit",
                "user_type": "nonprofit",
                "description": "Nonprofit organization account",
                "access_level": "Own campaigns only (limited access)",
            },
        ],
    }