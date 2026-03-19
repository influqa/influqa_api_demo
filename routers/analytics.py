"""Analytics router for the Influqa API demo."""

from fastapi import APIRouter, Depends, HTTPException, status

from auth import get_current_user
from data.sample_data import SAMPLE_ANALYTICS, SAMPLE_CAMPAIGNS
from models import CampaignAnalytics

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/campaigns/{campaign_id}",
    response_model=CampaignAnalytics,
    summary="Get Campaign Analytics",
    description=(
        "Retrieve performance analytics for a specific campaign. "
        "Includes reach, impressions, engagements, clicks, conversions, "
        "ROI, and per-influencer breakdowns."
    ),
)
def get_campaign_analytics(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    analytics = SAMPLE_ANALYTICS.get(campaign_id)
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analytics for campaign '{campaign_id}' not found. "
                   "Analytics are only available for active or completed campaigns.",
        )
    return CampaignAnalytics(**analytics)


@router.get(
    "/overview",
    summary="Get Account Overview",
    description=(
        "Retrieve a high-level overview of all campaign performance metrics "
        "for the authenticated brand/agency account."
    ),
)
def get_overview(current_user: dict = Depends(get_current_user)):
    brand_id = current_user["user_id"]
    brand_campaigns = [c for c in SAMPLE_CAMPAIGNS if c["brand_id"] == brand_id]
    campaign_ids = [c["id"] for c in brand_campaigns]

    total_reach = 0
    total_impressions = 0
    total_engagements = 0
    total_conversions = 0
    total_roi = []

    for cid in campaign_ids:
        data = SAMPLE_ANALYTICS.get(cid)
        if data:
            total_reach += data["total_reach"]
            total_impressions += data["total_impressions"]
            total_engagements += data["total_engagements"]
            total_conversions += data["total_conversions"]
            total_roi.append(data["roi"])

    avg_roi = round(sum(total_roi) / len(total_roi), 2) if total_roi else 0.0
    avg_engagement = (
        round(total_engagements / total_impressions * 100, 2) if total_impressions else 0.0
    )

    return {
        "brand_id": brand_id,
        "total_campaigns": len(brand_campaigns),
        "active_campaigns": sum(1 for c in brand_campaigns if c["status"] == "active"),
        "completed_campaigns": sum(1 for c in brand_campaigns if c["status"] == "completed"),
        "total_reach": total_reach,
        "total_impressions": total_impressions,
        "total_engagements": total_engagements,
        "average_engagement_rate": avg_engagement,
        "total_conversions": total_conversions,
        "average_roi": avg_roi,
    }
