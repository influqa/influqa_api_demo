"""Influencer discovery router for the Influqa API demo."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from models import Influencer, InfluencerListResponse
from auth import get_current_user
from data.sample_data import SAMPLE_INFLUENCERS
import math

router = APIRouter(prefix="/influencers", tags=["Influencer Discovery"])


def _filter_influencers(
    influencers: list[dict],
    niche: Optional[str],
    platform: Optional[str],
    min_followers: Optional[int],
    max_followers: Optional[int],
    min_engagement_rate: Optional[float],
    location: Optional[str],
    verified_only: bool,
    tags: Optional[str],
) -> list[dict]:
    results = influencers
    if niche:
        results = [i for i in results if i["niche"].lower() == niche.lower()]
    if platform:
        results = [i for i in results if i["platform"].lower() == platform.lower()]
    if min_followers is not None:
        results = [i for i in results if i["follower_count"] >= min_followers]
    if max_followers is not None:
        results = [i for i in results if i["follower_count"] <= max_followers]
    if min_engagement_rate is not None:
        results = [i for i in results if i["engagement_rate"] >= min_engagement_rate]
    if location:
        results = [
            i for i in results if location.lower() in i["location"].lower()
        ]
    if verified_only:
        results = [i for i in results if i["verified"]]
    if tags:
        tag_list = [t.strip().lower() for t in tags.split(",") if t.strip()]
        results = [
            i
            for i in results
            if any(t in [tag.lower() for tag in i["tags"]] for t in tag_list)
        ]
    return results


@router.get(
    "",
    response_model=InfluencerListResponse,
    summary="Search Influencers",
    description=(
        "Search and filter the Influqa database of verified creators. "
        "Supports filtering by niche, platform, follower count, engagement rate, "
        "location, verification status, and tags."
    ),
)
def list_influencers(
    niche: Optional[str] = Query(None, description="Filter by content niche (e.g. lifestyle, fitness, beauty)"),
    platform: Optional[str] = Query(None, description="Filter by platform: instagram, youtube, tiktok"),
    min_followers: Optional[int] = Query(None, ge=0, description="Minimum follower count"),
    max_followers: Optional[int] = Query(None, ge=0, description="Maximum follower count"),
    min_engagement_rate: Optional[float] = Query(None, ge=0, description="Minimum engagement rate (%)"),
    location: Optional[str] = Query(None, description="Filter by location (city or country)"),
    verified_only: bool = Query(False, description="Return only Influqa-verified creators"),
    tags: Optional[str] = Query(None, description="Comma-separated list of tags to filter by"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Results per page"),
    current_user: dict = Depends(get_current_user),
):
    filtered = _filter_influencers(
        SAMPLE_INFLUENCERS, niche, platform, min_followers, max_followers,
        min_engagement_rate, location, verified_only, tags,
    )
    total = len(filtered)
    pages = math.ceil(total / per_page) if total else 1
    start = (page - 1) * per_page
    page_items = filtered[start : start + per_page]
    return InfluencerListResponse(
        influencers=[Influencer(**i) for i in page_items],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get(
    "/{influencer_id}",
    response_model=Influencer,
    summary="Get Influencer Profile",
    description="Retrieve the full profile of a specific influencer by their ID.",
)
def get_influencer(
    influencer_id: str,
    current_user: dict = Depends(get_current_user),
):
    match = next((i for i in SAMPLE_INFLUENCERS if i["id"] == influencer_id), None)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Influencer '{influencer_id}' not found.",
        )
    return Influencer(**match)
