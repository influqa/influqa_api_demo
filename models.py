"""
Pydantic models for the Influqa API demo.
"""

from __future__ import annotations
from datetime import date, datetime
from typing import Any, Optional
from pydantic import BaseModel, Field


# ── Auth ─────────────────────────────────────────────────────────────────────

class AuthResponse(BaseModel):
    user_id: str
    role: str
    company_name: str
    email: str
    message: str = "Authenticated successfully"


# ── Influencers ───────────────────────────────────────────────────────────────

class AudienceDemographics(BaseModel):
    age_18_24: float
    age_25_34: float
    age_35_44: float
    age_45_plus: float
    female: float
    male: float
    top_countries: list[str]


class Influencer(BaseModel):
    id: str
    username: str
    full_name: str
    platform: str
    niche: str
    follower_count: int
    engagement_rate: float
    average_likes: int
    average_comments: int
    location: str
    language: str
    profile_url: str
    avatar_url: str
    verified: bool
    tags: list[str]
    rate_per_post: float
    currency: str
    audience_demographics: AudienceDemographics


class InfluencerListResponse(BaseModel):
    influencers: list[Influencer]
    total: int
    page: int
    per_page: int
    pages: int


class InfluencerSearchParams(BaseModel):
    niche: Optional[str] = None
    platform: Optional[str] = None
    min_followers: Optional[int] = None
    max_followers: Optional[int] = None
    min_engagement_rate: Optional[float] = None
    location: Optional[str] = None
    verified_only: bool = False
    tags: Optional[list[str]] = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)


# ── Campaigns ─────────────────────────────────────────────────────────────────

class Deliverable(BaseModel):
    type: str
    count: int


class InfluencerRequirements(BaseModel):
    min_followers: int = 10000
    max_followers: Optional[int] = None
    min_engagement_rate: float = 2.0
    required_niches: list[str] = []
    preferred_locations: list[str] = []


class Campaign(BaseModel):
    id: str
    brand_id: str
    title: str
    description: str
    status: str
    niche: str
    platforms: list[str]
    budget: float
    currency: str
    influencer_requirements: InfluencerRequirements
    deliverables: list[Deliverable]
    start_date: str
    end_date: str
    created_at: str
    updated_at: str
    applications_count: int
    hired_count: int


class CampaignCreateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    niche: str
    platforms: list[str]
    budget: float = Field(..., gt=0)
    currency: str = "USD"
    influencer_requirements: InfluencerRequirements = Field(
        default_factory=InfluencerRequirements
    )
    deliverables: list[Deliverable] = []
    start_date: str
    end_date: str


class CampaignListResponse(BaseModel):
    campaigns: list[Campaign]
    total: int
    page: int
    per_page: int
    pages: int


# ── Analytics ─────────────────────────────────────────────────────────────────

class InfluencerPerformance(BaseModel):
    influencer_id: str
    reach: int
    impressions: int
    engagements: int
    clicks: int
    conversions: int


class CampaignAnalytics(BaseModel):
    campaign_id: str
    total_reach: int
    total_impressions: int
    total_engagements: int
    engagement_rate: float
    total_clicks: int
    click_through_rate: float
    total_conversions: int
    conversion_rate: float
    cost_per_click: float
    cost_per_conversion: float
    roi: float
    influencer_performance: list[InfluencerPerformance]


# ── Common ────────────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


class SuccessResponse(BaseModel):
    message: str
    data: Optional[Any] = None
