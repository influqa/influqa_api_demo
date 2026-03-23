"""
Pydantic models for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date


# ============== User Types ==============

class UserBase(BaseModel):
    """Base user information"""
    user_id: str
    user_type: str = Field(..., description="User type: brand, agency, influencer, creator, business, nonprofit, education, admin")


class UserAccess(BaseModel):
    """User access summary"""
    user_type: str
    accessible_influencers: int
    accessible_campaigns: int
    accessible_offers: int
    permissions: List[str]


# ============== Influencer Models ==============

class InfluencerList(BaseModel):
    """List of influencers response"""
    success: bool
    count: int
    user_type: str
    access_level: str
    data: List[Dict[str, Any]]


class InfluencerDetail(BaseModel):
    """Single influencer detail response"""
    success: bool
    user_type: str
    data: Dict[str, Any]


class Influencer(BaseModel):
    """Influencer profile"""
    id: str
    username: str
    full_name: str
    email: Optional[str] = None
    platform: str
    niche: str
    follower_count: int
    engagement_rate: float
    average_likes: int
    average_comments: int
    location: str
    language: str
    profile_url: str
    avatar_url: Optional[str] = None
    verified: bool
    tags: List[str]
    rate_per_post: int
    currency: str = "USD"
    agency_id: Optional[str] = None


# ============== Campaign Models ==============

class CampaignList(BaseModel):
    """List of campaigns response"""
    success: bool
    count: int
    user_type: str
    access_level: str
    data: List[Dict[str, Any]]


class Campaign(BaseModel):
    """Campaign details"""
    id: str
    brand_id: str
    title: str
    description: str
    status: str
    niche: str
    platforms: List[str]
    budget: int
    currency: str = "USD"
    influencer_requirements: Dict[str, Any]
    deliverables: List[Dict[str, Any]]
    hired_influencer_ids: List[str] = []
    start_date: str
    end_date: str
    created_at: str
    updated_at: str


class Deliverable(BaseModel):
    """Campaign deliverable"""
    type: str = Field(..., description="Type: feed_post, story, reel, video_review")
    count: int
    description: Optional[str] = None


class InfluencerRequirements(BaseModel):
    """Campaign influencer requirements"""
    min_followers: Optional[int] = None
    max_followers: Optional[int] = None
    min_engagement_rate: Optional[float] = None
    required_niches: List[str] = []
    preferred_locations: List[str] = []


class CampaignCreate(BaseModel):
    """Create campaign request"""
    title: str
    description: str
    niche: str
    platforms: List[str]
    budget: int
    currency: Optional[str] = "USD"
    influencer_requirements: InfluencerRequirements
    deliverables: List[Deliverable]
    start_date: str
    end_date: str


# ============== Offer Models ==============

class Offer(BaseModel):
    """Offer details"""
    id: str
    campaign_id: str
    brand_id: str
    influencer_id: str
    status: str = Field(..., description="Status: pending, accepted, declined, completed")
    offer_type: str = Field(..., description="Type: paid, barter, affiliate")
    amount: int
    currency: str = "USD"
    deliverables: List[Dict[str, Any]]
    message: Optional[str] = None
    created_at: str
    updated_at: str


class OfferCreate(BaseModel):
    """Create offer request"""
    campaign_id: str
    influencer_id: str
    offer_type: str = "paid"
    amount: int
    currency: Optional[str] = "USD"
    deliverables: List[Deliverable]
    message: Optional[str] = None


# ============== Analytics Models ==============

class AnalyticsOverview(BaseModel):
    """Analytics overview response"""
    success: bool
    data: Dict[str, Any]


class CampaignAnalytics(BaseModel):
    """Campaign analytics response"""
    success: bool
    user_type: str
    campaign: Dict[str, Any]
    data: Dict[str, Any]


class InfluencerAnalytics(BaseModel):
    """Influencer analytics response"""
    success: bool
    user_type: str
    influencer: Dict[str, Any]
    data: Dict[str, Any]


# ============== Auth Models ==============

class AuthVerifyResponse(BaseModel):
    """Auth verification response"""
    success: bool
    message: str
    user: Dict[str, Any]
    access_summary: Dict[str, Any]


class DemoKey(BaseModel):
    """Demo API key info"""
    api_key: str
    user_type: str
    description: str
    access_level: str


class DemoKeysResponse(BaseModel):
    """List of demo keys response"""
    success: bool
    message: str
    demo_keys: List[DemoKey]


# ============== Error Models ==============

class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_code: Optional[str] = None