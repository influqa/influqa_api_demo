"""
Analytics endpoints with role-based access control.

Access by user type:
- admin: Full access to all analytics
- brand/business/nonprofit/education: Analytics for their own campaigns
- agency: Analytics for campaigns their managed influencers are part of
- influencer/creator: Analytics for campaigns they're hired in
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from data.sample_data import (
    SAMPLE_ANALYTICS,
    SAMPLE_CAMPAIGNS,
    SAMPLE_INFLUENCERS,
    get_user_accessible_campaign_ids,
    get_user_accessible_influencer_ids,
)
from auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
async def get_analytics_overview(
    user: dict = get_current_user,
):
    """
    Get analytics overview based on user access level.
    
    **Access Control:**
    - **admin**: Overview of all platform analytics
    - **brand/business/nonprofit/education**: Overview of their campaigns
    - **agency**: Overview of campaigns their influencers are in
    - **influencer/creator**: Overview of their own performance
    """
    accessible_campaign_ids = get_user_accessible_campaign_ids(user)
    accessible_influencer_ids = get_user_accessible_influencer_ids(user)
    
    # Aggregate analytics
    total_reach = 0
    total_impressions = 0
    total_engagements = 0
    total_clicks = 0
    total_conversions = 0
    total_spend = 0
    
    for camp_id in accessible_campaign_ids:
        if camp_id in SAMPLE_ANALYTICS:
            analytics = SAMPLE_ANALYTICS[camp_id]
            total_reach += analytics["total_reach"]
            total_impressions += analytics["total_impressions"]
            total_engagements += analytics["total_engagements"]
            total_clicks += analytics["total_clicks"]
            total_conversions += analytics["total_conversions"]
            
            # Get campaign budget
            camp = next((c for c in SAMPLE_CAMPAIGNS if c["id"] == camp_id), None)
            if camp:
                total_spend += camp.get("budget", 0)
    
    # Calculate rates
    engagement_rate = (total_engagements / total_impressions * 100) if total_impressions > 0 else 0
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    roi = ((total_conversions * 50 - total_spend) / total_spend * 100) if total_spend > 0 else 0  # Assuming $50 per conversion
    
    overview = {
        "user_type": user["user_type"],
        "accessible_campaigns": len(accessible_campaign_ids),
        "accessible_influencers": len(accessible_influencer_ids),
        "metrics": {
            "total_reach": total_reach,
            "total_impressions": total_impressions,
            "total_engagements": total_engagements,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "total_spend": total_spend,
            "engagement_rate": round(engagement_rate, 2),
            "click_through_rate": round(ctr, 2),
            "conversion_rate": round(conversion_rate, 2),
            "roi": round(roi, 2),
        },
    }
    
    # Add influencer-specific metrics
    if user["user_type"] in ["influencer", "creator"]:
        influencer_id = user.get("user_id")
        if influencer_id in accessible_influencer_ids:
            inf = next((i for i in SAMPLE_INFLUENCERS if i["id"] == influencer_id), None)
            if inf:
                overview["influencer_profile"] = {
                    "username": inf["username"],
                    "follower_count": inf["follower_count"],
                    "engagement_rate": inf["engagement_rate"],
                    "total_campaigns": len(accessible_campaign_ids),
                }
    
    # Add agency-specific metrics
    if user["user_type"] == "agency":
        overview["agency_metrics"] = {
            "managed_influencers": len(user.get("managed_influencer_ids", [])),
            "active_campaigns": len([c for c in SAMPLE_CAMPAIGNS if c["id"] in accessible_campaign_ids and c["status"] == "active"]),
        }
    
    return {
        "success": True,
        "data": overview,
    }


@router.get("/campaigns/{campaign_id}")
async def get_campaign_analytics(
    campaign_id: str,
    user: dict = get_current_user,
):
    """
    Get detailed analytics for a specific campaign.
    
    **Access Control:** Only accessible if:
    - You are an admin, OR
    - You own this campaign (brand/business/nonprofit/education), OR
    - Your managed influencers are in this campaign (agency), OR
    - You are hired in this campaign (influencer/creator)
    """
    accessible_ids = get_user_accessible_campaign_ids(user)
    
    if campaign_id not in accessible_ids:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied. You don't have permission to view analytics for campaign {campaign_id}.",
        )
    
    campaign = next((camp for camp in SAMPLE_CAMPAIGNS if camp["id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    analytics = SAMPLE_ANALYTICS.get(campaign_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="Analytics not found for this campaign")
    
    # Filter influencer performance based on user access
    accessible_influencer_ids = get_user_accessible_influencer_ids(user)
    
    if user["user_type"] == "admin":
        # Admin sees all influencer performance
        filtered_performance = analytics.get("influencer_performance", [])
    else:
        # Others see only accessible influencers
        filtered_performance = [
            perf for perf in analytics.get("influencer_performance", [])
            if perf["influencer_id"] in accessible_influencer_ids
        ]
    
    # Enrich influencer performance with names
    enriched_performance = []
    for perf in filtered_performance:
        inf = next((i for i in SAMPLE_INFLUENCERS if i["id"] == perf["influencer_id"]), None)
        enriched_performance.append({
            **perf,
            "influencer_username": inf["username"] if inf else "Unknown",
            "influencer_name": inf["full_name"] if inf else "Unknown",
        })
    
    return {
        "success": True,
        "user_type": user["user_type"],
        "campaign": {
            "id": campaign["id"],
            "title": campaign["title"],
            "status": campaign["status"],
            "budget": campaign["budget"],
        },
        "data": {
            **analytics,
            "influencer_performance": enriched_performance,
        },
    }


@router.get("/influencers/{influencer_id}")
async def get_influencer_analytics(
    influencer_id: str,
    user: dict = get_current_user,
):
    """
    Get analytics for a specific influencer.
    
    **Access Control:**
    - **admin**: See analytics for any influencer
    - **agency**: See analytics for influencers you manage
    - **brand/business**: See analytics for influencers you work with
    - **influencer/creator**: See only your own analytics
    - **nonprofit/education**: No access
    """
    accessible_ids = get_user_accessible_influencer_ids(user)
    
    if influencer_id not in accessible_ids:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied. You don't have permission to view analytics for influencer {influencer_id}.",
        )
    
    influencer = next((inf for inf in SAMPLE_INFLUENCERS if inf["id"] == influencer_id), None)
    if not influencer:
        raise HTTPException(status_code=404, detail="Influencer not found")
    
    # Aggregate influencer's campaign performance
    campaign_performance = []
    for camp_id, analytics in SAMPLE_ANALYTICS.items():
        for perf in analytics.get("influencer_performance", []):
            if perf["influencer_id"] == influencer_id:
                camp = next((c for c in SAMPLE_CAMPAIGNS if c["id"] == camp_id), None)
                if camp:
                    campaign_performance.append({
                        "campaign_id": camp_id,
                        "campaign_title": camp["title"],
                        "campaign_status": camp["status"],
                        "reach": perf["reach"],
                        "impressions": perf["impressions"],
                        "engagements": perf["engagements"],
                        "clicks": perf["clicks"],
                        "conversions": perf["conversions"],
                    })
    
    # Calculate totals
    total_reach = sum(p["reach"] for p in campaign_performance)
    total_impressions = sum(p["impressions"] for p in campaign_performance)
    total_engagements = sum(p["engagements"] for p in campaign_performance)
    
    return {
        "success": True,
        "user_type": user["user_type"],
        "influencer": {
            "id": influencer["id"],
            "username": influencer["username"],
            "full_name": influencer["full_name"],
            "follower_count": influencer["follower_count"],
            "engagement_rate": influencer["engagement_rate"],
        },
        "data": {
            "total_campaigns": len(campaign_performance),
            "total_reach": total_reach,
            "total_impressions": total_impressions,
            "total_engagements": total_engagements,
            "campaigns": campaign_performance,
        },
    }