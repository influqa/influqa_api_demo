"""
Campaign management endpoints with role-based access control.

Access by user type:
- business/nonprofit/education: Access to their own campaigns only
- agency: Access to campaigns where their managed influencers are hired
- influencer: Access to campaigns they're part of
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import date
from data.sample_data import (
    SAMPLE_CAMPAIGNS,
    SAMPLE_INFLUENCERS,
    SAMPLE_OFFERS,
    get_user_accessible_campaign_ids,
    get_user_accessible_influencer_ids,
)
from auth import get_current_user
from models import Campaign, CampaignList, CampaignCreate

router = APIRouter(prefix="/campaigns", tags=["Campaign Management"])


@router.get("", response_model=CampaignList)
async def list_campaigns(
    status: Optional[str] = Query(None, description="Filter by status: active, completed, draft, paused"),
    niche: Optional[str] = Query(None, description="Filter by niche"),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    user: dict = get_current_user,
):
    """
    List campaigns based on user access level.
    
    **Access Control:**
    - **business/nonprofit/education**: See your own campaigns only
    - **agency**: See campaigns where your managed influencers are hired
    - **influencer**: See campaigns you're hired for
    """
    accessible_ids = get_user_accessible_campaign_ids(user)
    
    # Filter campaigns by access level
    campaigns = [camp for camp in SAMPLE_CAMPAIGNS if camp["id"] in accessible_ids]
    
    # Apply additional filters
    if status:
        campaigns = [camp for camp in campaigns if camp["status"] == status.lower()]
    if niche:
        campaigns = [camp for camp in campaigns if niche.lower() in camp.get("niche", "").lower()]
    if platform:
        campaigns = [camp for camp in campaigns if platform.lower() in [p.lower() for p in camp.get("platforms", [])]]
    
    return {
        "success": True,
        "count": len(campaigns),
        "user_type": user["user_type"],
        "access_level": "limited",
        "data": campaigns,
    }


@router.get("/{campaign_id}")
async def get_campaign(
    campaign_id: str,
    user: dict = get_current_user,
):
    """
    Get detailed information about a specific campaign.
    
    **Access Control:** Only accessible if:
    - You own this campaign (business/nonprofit/education), OR
    - Your managed influencers are in this campaign (agency), OR
    - You are hired in this campaign (influencer)
    """
    accessible_ids = get_user_accessible_campaign_ids(user)
    
    if campaign_id not in accessible_ids:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied. You don't have permission to view campaign {campaign_id}.",
        )
    
    campaign = next((camp for camp in SAMPLE_CAMPAIGNS if camp["id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Get influencer details for hired influencers
    hired_influencers = []
    accessible_influencer_ids = get_user_accessible_influencer_ids(user)
    for inf_id in campaign.get("hired_influencer_ids", []):
        inf = next((i for i in SAMPLE_INFLUENCERS if i["id"] == inf_id), None)
        if inf:
            # Only show full details if user has access to this influencer
            if inf_id in accessible_influencer_ids:
                hired_influencers.append({
                    "id": inf["id"],
                    "username": inf["username"],
                    "full_name": inf["full_name"],
                    "platform": inf["platform"],
                    "follower_count": inf["follower_count"],
                    "engagement_rate": inf["engagement_rate"],
                })
            else:
                # Limited info
                hired_influencers.append({
                    "id": inf["id"],
                    "username": inf["username"],
                    "platform": inf["platform"],
                })
    
    # Get offers for this campaign
    campaign_offers = [off for off in SAMPLE_OFFERS if off["campaign_id"] == campaign_id]
    
    return {
        "success": True,
        "user_type": user["user_type"],
        "data": {
            **campaign,
            "hired_influencers": hired_influencers,
            "offers": campaign_offers,
        },
    }


@router.post("")
async def create_campaign(
    campaign_data: CampaignCreate,
    user: dict = get_current_user,
):
    """
    Create a new campaign.
    
    **Access Control:**
    - **business, nonprofit, education**: Can create campaigns
    - **agency, influencer**: Cannot create campaigns
    """
    if user["user_type"] not in ["business", "nonprofit", "education"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only businesses and organizations can create campaigns.",
        )
    
    # In a real app, this would save to database
    new_campaign = {
        "id": f"camp_new_{len(SAMPLE_CAMPAIGNS) + 1}",
        "brand_id": user["user_id"],
        "title": campaign_data.title,
        "description": campaign_data.description,
        "status": "draft",
        "niche": campaign_data.niche,
        "platforms": campaign_data.platforms,
        "budget": campaign_data.budget,
        "currency": campaign_data.currency or "USD",
        "influencer_requirements": campaign_data.influencer_requirements,
        "deliverables": campaign_data.deliverables,
        "hired_influencer_ids": [],
        "start_date": campaign_data.start_date,
        "end_date": campaign_data.end_date,
        "created_at": date.today().isoformat(),
        "updated_at": date.today().isoformat(),
        "applications_count": 0,
        "hired_count": 0,
    }
    
    return {
        "success": True,
        "message": "Campaign created successfully",
        "data": new_campaign,
    }


@router.patch("/{campaign_id}/status")
async def update_campaign_status(
    campaign_id: str,
    status: str = Query(..., description="New status: active, paused, completed, cancelled"),
    user: dict = get_current_user,
):
    """
    Update campaign status.
    
    **Access Control:**
    - **business/nonprofit/education**: Can update their own campaigns only
    - **agency/influencer**: Cannot update campaign status
    """
    if user["user_type"] in ["agency", "influencer"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied. You cannot update campaign status.",
        )
    
    campaign = next((camp for camp in SAMPLE_CAMPAIGNS if camp["id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Check ownership
    if campaign["brand_id"] != user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied. You can only update your own campaigns.",
        )
    
    valid_statuses = ["active", "paused", "completed", "cancelled", "draft"]
    if status.lower() not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}",
        )
    
    return {
        "success": True,
        "message": f"Campaign status updated to {status}",
        "campaign_id": campaign_id,
        "old_status": campaign["status"],
        "new_status": status.lower(),
    }


@router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: str,
    user: dict = get_current_user,
):
    """
    Delete a campaign.
    
    **Access Control:**
    - **business/nonprofit/education**: Can delete their own campaigns only
    - **agency/influencer**: Cannot delete campaigns
    """
    if user["user_type"] in ["agency", "influencer"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied. You cannot delete campaigns.",
        )
    
    campaign = next((camp for camp in SAMPLE_CAMPAIGNS if camp["id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    # Check ownership
    if campaign["brand_id"] != user["user_id"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied. You can only delete your own campaigns.",
        )
    
    # Check if campaign has hired influencers
    if campaign.get("hired_influencer_ids"):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete campaign with hired influencers. Please complete or cancel the campaign first.",
        )
    
    return {
        "success": True,
        "message": "Campaign deleted successfully",
        "campaign_id": campaign_id,
    }