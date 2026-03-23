"""
Influencer discovery endpoints with role-based access control.

Access by user type:
- business: Access to influencers they work with (hired in their campaigns)
- agency: Access to influencers they manage only
- influencer: Access to their own profile only
- nonprofit/education: No influencer access
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from data.sample_data import (
    SAMPLE_INFLUENCERS, 
    get_user_accessible_influencer_ids,
    get_user_accessible_campaign_ids,
    SAMPLE_CAMPAIGNS,
    SAMPLE_OFFERS,
)
from auth import get_current_user
from models import Influencer, InfluencerList, InfluencerDetail

router = APIRouter(prefix="/influencers", tags=["Influencer Discovery"])


@router.get("", response_model=InfluencerList)
async def list_influencers(
    niche: Optional[str] = Query(None, description="Filter by niche"),
    platform: Optional[str] = Query(None, description="Filter by platform (instagram, youtube, tiktok)"),
    min_followers: Optional[int] = Query(None, description="Minimum follower count"),
    max_followers: Optional[int] = Query(None, description="Maximum follower count"),
    min_engagement: Optional[float] = Query(None, description="Minimum engagement rate"),
    location: Optional[str] = Query(None, description="Filter by location"),
    user: dict = get_current_user,
):
    """
    List influencers based on user access level.
    
    **Access Control:**
    - **business**: See influencers you work with
    - **agency**: See only influencers you manage
    - **influencer**: See only your own profile
    - **nonprofit/education**: No access (returns empty list)
    """
    accessible_ids = get_user_accessible_influencer_ids(user)
    
    # Filter influencers by access level
    influencers = [inf for inf in SAMPLE_INFLUENCERS if inf["id"] in accessible_ids]
    
    # Apply additional filters
    if niche:
        influencers = [inf for inf in influencers if niche.lower() in [t.lower() for t in inf.get("tags", [])]]
    if platform:
        influencers = [inf for inf in influencers if inf["platform"].lower() == platform.lower()]
    if min_followers:
        influencers = [inf for inf in influencers if inf["follower_count"] >= min_followers]
    if max_followers:
        influencers = [inf for inf in influencers if inf["follower_count"] <= max_followers]
    if min_engagement:
        influencers = [inf for inf in influencers if inf["engagement_rate"] >= min_engagement]
    if location:
        influencers = [inf for inf in influencers if location.lower() in inf["location"].lower()]
    
    return {
        "success": True,
        "count": len(influencers),
        "user_type": user["user_type"],
        "access_level": "limited",
        "data": influencers,
    }


@router.get("/{influencer_id}", response_model=InfluencerDetail)
async def get_influencer(
    influencer_id: str,
    user: dict = get_current_user,
):
    """
    Get detailed information about a specific influencer.
    
    **Access Control:** Only accessible if:
    - You manage this influencer (agency), OR
    - You work with this influencer (business), OR
    - This is your own profile (influencer)
    """
    accessible_ids = get_user_accessible_influencer_ids(user)
    
    if influencer_id not in accessible_ids:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied. You don't have permission to view influencer {influencer_id}.",
        )
    
    influencer = next((inf for inf in SAMPLE_INFLUENCERS if inf["id"] == influencer_id), None)
    if not influencer:
        raise HTTPException(status_code=404, detail="Influencer not found")
    
    # Get campaigns this influencer is part of
    campaign_ids = get_user_accessible_campaign_ids(user)
    influencer_campaigns = [
        {"id": camp["id"], "title": camp["title"], "status": camp["status"]}
        for camp in SAMPLE_CAMPAIGNS
        if influencer_id in camp.get("hired_influencer_ids", []) and camp["id"] in campaign_ids
    ]
    
    # Get offers for this influencer (if user has access)
    accessible_offer_ids = []
    user_type = user["user_type"]
    if user_type == "agency" and influencer_id in user.get("managed_influencer_ids", []):
        accessible_offer_ids = [off["id"] for off in SAMPLE_OFFERS if off["influencer_id"] == influencer_id]
    elif user_type == "influencer" and user.get("user_id") == influencer_id:
        accessible_offer_ids = [off["id"] for off in SAMPLE_OFFERS if off["influencer_id"] == influencer_id]
    
    influencer_offers = [
        {
            "id": off["id"],
            "campaign_title": next((c["title"] for c in SAMPLE_CAMPAIGNS if c["id"] == off["campaign_id"]), "Unknown"),
            "status": off["status"],
            "amount": off["amount"],
            "currency": off["currency"],
        }
        for off in SAMPLE_OFFERS
        if off["id"] in accessible_offer_ids
    ]
    
    return {
        "success": True,
        "user_type": user["user_type"],
        "data": {
            **influencer,
            "campaigns": influencer_campaigns,
            "offers": influencer_offers,
        },
    }


@router.get("/{influencer_id}/offers")
async def get_influencer_offers(
    influencer_id: str,
    status: Optional[str] = Query(None, description="Filter by status: pending, accepted, declined, completed"),
    user: dict = get_current_user,
):
    """
    Get offers for a specific influencer.
    
    **Access Control:**
    - **agency**: See offers for influencers you manage
    - **influencer**: See your own offers only
    - **Others**: No access
    """
    accessible_ids = get_user_accessible_influencer_ids(user)
    
    if influencer_id not in accessible_ids:
        raise HTTPException(
            status_code=403,
            detail="Access denied. You don't have permission to view this influencer's offers.",
        )
    
    offers = [off for off in SAMPLE_OFFERS if off["influencer_id"] == influencer_id]
    
    if status:
        offers = [off for off in offers if off["status"] == status.lower()]
    
    # Enrich with campaign info
    enriched_offers = []
    for offer in offers:
        campaign = next((c for c in SAMPLE_CAMPAIGNS if c["id"] == offer["campaign_id"]), None)
        enriched_offers.append({
            **offer,
            "campaign_title": campaign["title"] if campaign else "Unknown Campaign",
        })
    
    return {
        "success": True,
        "count": len(enriched_offers),
        "influencer_id": influencer_id,
        "user_type": user["user_type"],
        "data": enriched_offers,
    }