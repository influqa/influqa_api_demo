"""Campaign management router for the Influqa API demo."""

import math
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth import get_current_user
from data.sample_data import SAMPLE_CAMPAIGNS
from models import Campaign, CampaignCreateRequest, CampaignListResponse, SuccessResponse

router = APIRouter(prefix="/campaigns", tags=["Campaign Management"])

# In-memory store for demo purposes (extends the sample data)
_campaigns: list[dict] = list(SAMPLE_CAMPAIGNS)


@router.get(
    "",
    response_model=CampaignListResponse,
    summary="List Campaigns",
    description=(
        "List all campaigns associated with the authenticated brand/agency account. "
        "Supports filtering by status and niche."
    ),
)
def list_campaigns(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status: draft, active, completed, paused"),
    niche: Optional[str] = Query(None, description="Filter by campaign niche"),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    results = list(_campaigns)
    brand_id = current_user["user_id"]
    results = [c for c in results if c["brand_id"] == brand_id]

    if status_filter:
        results = [c for c in results if c["status"] == status_filter]
    if niche:
        results = [c for c in results if c["niche"].lower() == niche.lower()]

    total = len(results)
    pages = math.ceil(total / per_page) if total else 1
    start = (page - 1) * per_page
    page_items = results[start : start + per_page]

    return CampaignListResponse(
        campaigns=[Campaign(**c) for c in page_items],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.post(
    "",
    response_model=Campaign,
    status_code=status.HTTP_201_CREATED,
    summary="Create Campaign",
    description=(
        "Create a new influencer marketing campaign. "
        "Specify your target niche, platforms, budget, influencer requirements, "
        "and deliverables."
    ),
)
def create_campaign(
    payload: CampaignCreateRequest,
    current_user: dict = Depends(get_current_user),
):
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    new_campaign = {
        "id": f"camp_{uuid.uuid4().hex[:8]}",
        "brand_id": current_user["user_id"],
        "title": payload.title,
        "description": payload.description,
        "status": "draft",
        "niche": payload.niche,
        "platforms": payload.platforms,
        "budget": payload.budget,
        "currency": payload.currency,
        "influencer_requirements": payload.influencer_requirements.model_dump(),
        "deliverables": [d.model_dump() for d in payload.deliverables],
        "start_date": payload.start_date,
        "end_date": payload.end_date,
        "created_at": now,
        "updated_at": now,
        "applications_count": 0,
        "hired_count": 0,
    }
    _campaigns.append(new_campaign)
    return Campaign(**new_campaign)


@router.get(
    "/{campaign_id}",
    response_model=Campaign,
    summary="Get Campaign",
    description="Retrieve the details of a specific campaign by its ID.",
)
def get_campaign(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    campaign = next((c for c in _campaigns if c["id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign '{campaign_id}' not found.",
        )
    return Campaign(**campaign)


@router.patch(
    "/{campaign_id}/status",
    response_model=Campaign,
    summary="Update Campaign Status",
    description=(
        "Update the status of a campaign. "
        "Valid statuses: draft → active → paused → completed."
    ),
)
def update_campaign_status(
    campaign_id: str,
    new_status: str = Query(..., alias="status", description="New status: draft, active, paused, completed"),
    current_user: dict = Depends(get_current_user),
):
    valid_statuses = {"draft", "active", "paused", "completed"}
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status '{new_status}'. Valid values: {sorted(valid_statuses)}",
        )
    campaign = next((c for c in _campaigns if c["id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign '{campaign_id}' not found.",
        )
    campaign["status"] = new_status
    campaign["updated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return Campaign(**campaign)


@router.delete(
    "/{campaign_id}",
    response_model=SuccessResponse,
    summary="Delete Campaign",
    description="Delete a draft campaign. Only campaigns in 'draft' status can be deleted.",
)
def delete_campaign(
    campaign_id: str,
    current_user: dict = Depends(get_current_user),
):
    campaign = next((c for c in _campaigns if c["id"] == campaign_id), None)
    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign '{campaign_id}' not found.",
        )
    if campaign["status"] != "draft":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only campaigns in 'draft' status can be deleted.",
        )
    _campaigns.remove(campaign)
    return SuccessResponse(message=f"Campaign '{campaign_id}' deleted successfully.")
