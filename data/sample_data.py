"""
Sample data for the Influqa API demo.
This module contains mock data representing users, influencers, campaigns, offers, and analytics.

User Types (from https://www.influqa.com/pricing):
- Influencer: Can see offers they received, campaigns they're part of
- Business: Can create campaigns, see influencers they work with
- Nonprofit: Limited access - own campaigns only
- Agency: Manages influencers, sees their offers and campaigns
- Education: Limited access - own campaigns only

VIP Tiers: Basic (FREE), SVIP ($4.99/mo), GVIP ($19.99/mo)
"""

from datetime import date, timedelta

# User types available on the platform (from pricing page)
USER_TYPES = ["influencer", "business", "nonprofit", "agency", "education"]

# VIP tiers available for each user type
VIP_TIERS = ["basic", "svip", "gvip"]

# Demo API keys mapped to user types
SAMPLE_USERS = {
    # Influencer - can see offers they received, their campaigns
    "demo_key_influencer": {
        "api_key": "demo_key_influencer",
        "user_id": "inf_001",  # Linked to influencer profile
        "user_type": "influencer",
        "vip_tier": "svip",
        "username": "lifestyle_with_emma",
        "email": "emma@example.com",
        "managed_influencer_ids": [],  # Only themselves
        "campaign_ids": ["camp_001"],  # Campaigns they're part of
    },
    # Business - can create campaigns, see influencers they work with
    "demo_key_business": {
        "api_key": "demo_key_business",
        "user_id": "user_business_001",
        "user_type": "business",
        "vip_tier": "gvip",
        "company_name": "Tech Startup Co.",
        "email": "marketing@techstartup.com",
        "managed_influencer_ids": ["inf_001", "inf_002"],  # Influencers they work with
        "campaign_ids": ["camp_001", "camp_002"],  # Their campaigns
    },
    # Agency - manages influencers, sees their offers
    "demo_key_agency": {
        "api_key": "demo_key_agency",
        "user_id": "user_agency_001",
        "user_type": "agency",
        "vip_tier": "gvip",
        "company_name": "Creative Talent Agency",
        "email": "bookings@creativetalent.com",
        "managed_influencer_ids": ["inf_001", "inf_002", "inf_005"],  # Influencers they manage
        "campaign_ids": [],  # Agencies don't own campaigns
    },
    # Nonprofit - limited access, own campaigns
    "demo_key_nonprofit": {
        "api_key": "demo_key_nonprofit",
        "user_id": "user_nonprofit_001",
        "user_type": "nonprofit",
        "vip_tier": "svip",
        "organization_name": "Green Earth Foundation",
        "email": "awareness@greenearth.org",
        "managed_influencer_ids": [],
        "campaign_ids": ["camp_003"],  # Their campaigns
    },
    # Education - similar to nonprofit
    "demo_key_education": {
        "api_key": "demo_key_education",
        "user_id": "user_education_001",
        "user_type": "education",
        "vip_tier": "basic",
        "organization_name": "State University Media Dept",
        "email": "media@stateuniversity.edu",
        "managed_influencer_ids": [],
        "campaign_ids": ["camp_004"],
    },
}

# Influencers - managed by agencies, discovered by businesses
SAMPLE_INFLUENCERS = [
    {
        "id": "inf_001",
        "username": "lifestyle_with_emma",
        "full_name": "Emma Johnson",
        "email": "emma@example.com",
        "platform": "instagram",
        "niche": "lifestyle",
        "follower_count": 285000,
        "engagement_rate": 4.7,
        "average_likes": 13395,
        "average_comments": 820,
        "location": "New York, USA",
        "language": "en",
        "profile_url": "https://instagram.com/lifestyle_with_emma",
        "avatar_url": "https://example.com/avatars/emma.jpg",
        "verified": True,
        "tags": ["lifestyle", "fashion", "travel", "wellness"],
        "rate_per_post": 2500,
        "currency": "USD",
        "agency_id": "user_agency_001",  # Managed by agency
        "audience_demographics": {
            "age_18_24": 32,
            "age_25_34": 41,
            "age_35_44": 18,
            "age_45_plus": 9,
            "female": 72,
            "male": 28,
            "top_countries": ["US", "UK", "CA", "AU"],
        },
    },
    {
        "id": "inf_002",
        "username": "tech_tales_marcus",
        "full_name": "Marcus Chen",
        "email": "marcus@example.com",
        "platform": "youtube",
        "niche": "technology",
        "follower_count": 512000,
        "engagement_rate": 6.2,
        "average_likes": 31744,
        "average_comments": 2850,
        "location": "San Francisco, USA",
        "language": "en",
        "profile_url": "https://youtube.com/@tech_tales_marcus",
        "avatar_url": "https://example.com/avatars/marcus.jpg",
        "verified": True,
        "tags": ["technology", "gadgets", "reviews", "AI"],
        "rate_per_post": 5000,
        "currency": "USD",
        "agency_id": "user_agency_001",  # Managed by agency
        "audience_demographics": {
            "age_18_24": 28,
            "age_25_34": 45,
            "age_35_44": 20,
            "age_45_plus": 7,
            "female": 35,
            "male": 65,
            "top_countries": ["US", "IN", "UK", "DE"],
        },
    },
    {
        "id": "inf_003",
        "username": "foodie_fiesta_sophia",
        "full_name": "Sophia Martinez",
        "email": "sophia@example.com",
        "platform": "tiktok",
        "niche": "food",
        "follower_count": 1200000,
        "engagement_rate": 8.9,
        "average_likes": 106800,
        "average_comments": 5400,
        "location": "Los Angeles, USA",
        "language": "en",
        "profile_url": "https://tiktok.com/@foodie_fiesta_sophia",
        "avatar_url": "https://example.com/avatars/sophia.jpg",
        "verified": True,
        "tags": ["food", "recipes", "cooking", "restaurants"],
        "rate_per_post": 8000,
        "currency": "USD",
        "agency_id": None,  # Independent
        "audience_demographics": {
            "age_18_24": 45,
            "age_25_34": 35,
            "age_35_44": 14,
            "age_45_plus": 6,
            "female": 63,
            "male": 37,
            "top_countries": ["US", "MX", "CA", "ES"],
        },
    },
    {
        "id": "inf_004",
        "username": "fit_life_alex",
        "full_name": "Alex Thompson",
        "email": "alex@example.com",
        "platform": "instagram",
        "niche": "fitness",
        "follower_count": 98000,
        "engagement_rate": 5.8,
        "average_likes": 5684,
        "average_comments": 310,
        "location": "Austin, USA",
        "language": "en",
        "profile_url": "https://instagram.com/fit_life_alex",
        "avatar_url": "https://example.com/avatars/alex.jpg",
        "verified": False,
        "tags": ["fitness", "health", "workout", "nutrition"],
        "rate_per_post": 800,
        "currency": "USD",
        "agency_id": None,  # Independent
        "audience_demographics": {
            "age_18_24": 38,
            "age_25_34": 42,
            "age_35_44": 15,
            "age_45_plus": 5,
            "female": 55,
            "male": 45,
            "top_countries": ["US", "CA", "AU", "UK"],
        },
    },
    {
        "id": "inf_005",
        "username": "beauty_by_nina",
        "full_name": "Nina Patel",
        "email": "nina@example.com",
        "platform": "instagram",
        "niche": "beauty",
        "follower_count": 420000,
        "engagement_rate": 5.1,
        "average_likes": 21420,
        "average_comments": 1050,
        "location": "London, UK",
        "language": "en",
        "profile_url": "https://instagram.com/beauty_by_nina",
        "avatar_url": "https://example.com/avatars/nina.jpg",
        "verified": True,
        "tags": ["beauty", "makeup", "skincare", "fashion"],
        "rate_per_post": 3500,
        "currency": "USD",
        "agency_id": "user_agency_001",  # Managed by agency
        "audience_demographics": {
            "age_18_24": 40,
            "age_25_34": 38,
            "age_35_44": 16,
            "age_45_plus": 6,
            "female": 88,
            "male": 12,
            "top_countries": ["UK", "US", "IN", "AU"],
        },
    },
]

# Campaigns - owned by businesses/nonprofits/education
SAMPLE_CAMPAIGNS = [
    {
        "id": "camp_001",
        "brand_id": "user_business_001",
        "title": "Summer Fashion Collection 2025",
        "description": "Promote our new summer fashion line targeting millennials and Gen Z",
        "status": "active",
        "niche": "fashion",
        "platforms": ["instagram", "tiktok"],
        "budget": 25000,
        "currency": "USD",
        "influencer_requirements": {
            "min_followers": 50000,
            "max_followers": 500000,
            "min_engagement_rate": 3.5,
            "required_niches": ["fashion", "lifestyle"],
            "preferred_locations": ["US", "UK", "CA"],
        },
        "deliverables": [
            {"type": "feed_post", "count": 2},
            {"type": "story", "count": 5},
            {"type": "reel", "count": 1},
        ],
        "hired_influencer_ids": ["inf_001", "inf_005"],
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=30)),
        "created_at": "2025-05-01T10:00:00Z",
        "updated_at": "2025-05-15T14:30:00Z",
        "applications_count": 12,
        "hired_count": 2,
    },
    {
        "id": "camp_002",
        "brand_id": "user_business_001",
        "title": "Tech Product Launch",
        "description": "Launch campaign for our new gadget",
        "status": "active",
        "niche": "technology",
        "platforms": ["youtube", "instagram"],
        "budget": 30000,
        "currency": "USD",
        "influencer_requirements": {
            "min_followers": 100000,
            "max_followers": 1000000,
            "min_engagement_rate": 5.0,
            "required_niches": ["technology", "gadgets"],
            "preferred_locations": ["US", "UK", "DE"],
        },
        "deliverables": [
            {"type": "video_review", "count": 1},
            {"type": "feed_post", "count": 2},
        ],
        "hired_influencer_ids": ["inf_002"],
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=45)),
        "created_at": "2025-06-01T08:00:00Z",
        "updated_at": "2025-06-15T12:00:00Z",
        "applications_count": 8,
        "hired_count": 1,
    },
    {
        "id": "camp_003",
        "brand_id": "user_nonprofit_001",
        "title": "Environmental Awareness Campaign",
        "description": "Spread awareness about ocean conservation",
        "status": "active",
        "niche": "lifestyle",
        "platforms": ["instagram", "tiktok"],
        "budget": 5000,
        "currency": "USD",
        "influencer_requirements": {
            "min_followers": 10000,
            "max_followers": 500000,
            "min_engagement_rate": 3.0,
            "required_niches": ["lifestyle", "travel", "nature"],
            "preferred_locations": ["US", "UK", "AU"],
        },
        "deliverables": [
            {"type": "feed_post", "count": 1},
            {"type": "story", "count": 3},
        ],
        "hired_influencer_ids": ["inf_001"],
        "start_date": str(date.today()),
        "end_date": str(date.today() + timedelta(days=60)),
        "created_at": "2025-06-10T10:00:00Z",
        "updated_at": "2025-06-10T10:00:00Z",
        "applications_count": 5,
        "hired_count": 1,
    },
    {
        "id": "camp_004",
        "brand_id": "user_education_001",
        "title": "University Open Day Promotion",
        "description": "Promote upcoming university open day event",
        "status": "draft",
        "niche": "education",
        "platforms": ["instagram"],
        "budget": 2000,
        "currency": "USD",
        "influencer_requirements": {
            "min_followers": 5000,
            "max_followers": 100000,
            "min_engagement_rate": 4.0,
            "required_niches": ["education", "lifestyle"],
            "preferred_locations": ["US"],
        },
        "deliverables": [
            {"type": "story", "count": 3},
        ],
        "hired_influencer_ids": [],
        "start_date": str(date.today() + timedelta(days=30)),
        "end_date": str(date.today() + timedelta(days=45)),
        "created_at": "2025-06-20T09:00:00Z",
        "updated_at": "2025-06-20T09:00:00Z",
        "applications_count": 0,
        "hired_count": 0,
    },
]

# Offers - collaborations between businesses and influencers
SAMPLE_OFFERS = [
    {
        "id": "offer_001",
        "campaign_id": "camp_001",
        "brand_id": "user_business_001",
        "influencer_id": "inf_001",
        "status": "accepted",
        "offer_type": "paid",
        "amount": 5000,
        "currency": "USD",
        "deliverables": [
            {"type": "feed_post", "count": 2, "description": "Summer collection showcase"},
            {"type": "story", "count": 5, "description": "Behind the scenes content"},
        ],
        "message": "We'd love to have you as part of our summer campaign!",
        "created_at": "2025-05-02T14:00:00Z",
        "updated_at": "2025-05-03T10:30:00Z",
        "accepted_at": "2025-05-03T10:30:00Z",
    },
    {
        "id": "offer_002",
        "campaign_id": "camp_001",
        "brand_id": "user_business_001",
        "influencer_id": "inf_005",
        "status": "accepted",
        "offer_type": "paid",
        "amount": 7000,
        "currency": "USD",
        "deliverables": [
            {"type": "feed_post", "count": 2, "description": "Beauty product integration"},
            {"type": "reel", "count": 1, "description": "Tutorial video"},
        ],
        "message": "Perfect fit for our summer beauty collection!",
        "created_at": "2025-05-02T14:00:00Z",
        "updated_at": "2025-05-04T09:00:00Z",
        "accepted_at": "2025-05-04T09:00:00Z",
    },
    {
        "id": "offer_003",
        "campaign_id": "camp_002",
        "brand_id": "user_business_001",
        "influencer_id": "inf_002",
        "status": "pending",
        "offer_type": "paid",
        "amount": 8000,
        "currency": "USD",
        "deliverables": [
            {"type": "video_review", "count": 1, "description": "In-depth tech review"},
        ],
        "message": "Your tech reviews are amazing! Would you review our new gadget?",
        "created_at": "2025-06-16T09:00:00Z",
        "updated_at": "2025-06-16T09:00:00Z",
    },
    {
        "id": "offer_004",
        "campaign_id": "camp_003",
        "brand_id": "user_nonprofit_001",
        "influencer_id": "inf_001",
        "status": "pending",
        "offer_type": "paid",
        "amount": 1500,
        "currency": "USD",
        "deliverables": [
            {"type": "feed_post", "count": 1, "description": "Ocean conservation post"},
            {"type": "story", "count": 3, "description": "Awareness stories"},
        ],
        "message": "Help us spread awareness about ocean conservation!",
        "created_at": "2025-06-15T11:00:00Z",
        "updated_at": "2025-06-15T11:00:00Z",
    },
]

# Analytics data
SAMPLE_ANALYTICS = {
    "camp_001": {
        "campaign_id": "camp_001",
        "total_reach": 850000,
        "total_impressions": 2100000,
        "total_engagements": 42000,
        "engagement_rate": 2.0,
        "total_clicks": 8500,
        "click_through_rate": 0.4,
        "total_conversions": 340,
        "conversion_rate": 4.0,
        "cost_per_click": 2.94,
        "cost_per_conversion": 73.53,
        "roi": 180,
        "influencer_performance": [
            {
                "influencer_id": "inf_001",
                "reach": 280000,
                "impressions": 700000,
                "engagements": 14000,
                "clicks": 2800,
                "conversions": 112,
            },
            {
                "influencer_id": "inf_005",
                "reach": 420000,
                "impressions": 1000000,
                "engagements": 21000,
                "clicks": 4200,
                "conversions": 168,
            },
        ],
    },
    "camp_002": {
        "campaign_id": "camp_002",
        "total_reach": 520000,
        "total_impressions": 1200000,
        "total_engagements": 72000,
        "engagement_rate": 6.0,
        "total_clicks": 12000,
        "click_through_rate": 1.0,
        "total_conversions": 480,
        "conversion_rate": 4.0,
        "cost_per_click": 2.50,
        "cost_per_conversion": 62.50,
        "roi": 250,
        "influencer_performance": [
            {
                "influencer_id": "inf_002",
                "reach": 520000,
                "impressions": 1200000,
                "engagements": 72000,
                "clicks": 12000,
                "conversions": 480,
            },
        ],
    },
}

# Access control helper functions
def get_user_accessible_influencer_ids(user: dict) -> list:
    """
    Get list of influencer IDs the user can access.
    
    Access rules:
    - business: Influencers they work with (managed_influencer_ids)
    - agency: Influencers they manage
    - influencer: Only themselves (if they have an influencer profile)
    - nonprofit/education: Empty (no direct influencer access)
    """
    user_type = user.get("user_type")
    
    if user_type == "business":
        return user.get("managed_influencer_ids", [])
    
    if user_type == "agency":
        return user.get("managed_influencer_ids", [])
    
    if user_type == "influencer":
        # Return only their own influencer profile ID
        user_id = user.get("user_id")
        if user_id.startswith("inf_"):
            return [user_id]
        return []
    
    return []  # nonprofit, education have no influencer access


def get_user_accessible_campaign_ids(user: dict) -> list:
    """
    Get list of campaign IDs the user can access.
    
    Access rules:
    - business/nonprofit/education: Their own campaigns
    - agency: Campaigns where their managed influencers are hired
    - influencer: Campaigns they're hired for
    """
    user_type = user.get("user_type")
    
    if user_type in ["business", "nonprofit", "education"]:
        return user.get("campaign_ids", [])
    
    if user_type == "agency":
        # Campaigns where their managed influencers are hired
        managed_ids = set(user.get("managed_influencer_ids", []))
        campaign_ids = []
        for camp in SAMPLE_CAMPAIGNS:
            hired = set(camp.get("hired_influencer_ids", []))
            if hired & managed_ids:  # Intersection
                campaign_ids.append(camp["id"])
        return campaign_ids
    
    if user_type == "influencer":
        # Campaigns they're hired for
        influencer_id = user.get("user_id")
        campaign_ids = []
        for camp in SAMPLE_CAMPAIGNS:
            if influencer_id in camp.get("hired_influencer_ids", []):
                campaign_ids.append(camp["id"])
        return campaign_ids
    
    return []


def get_user_accessible_offer_ids(user: dict) -> list:
    """
    Get list of offer IDs the user can access.
    
    Access rules:
    - business: Offers they sent
    - agency: Offers for their managed influencers
    - influencer: Offers they received
    - nonprofit/education: Offers they sent
    """
    user_type = user.get("user_type")
    user_id = user.get("user_id")
    
    if user_type in ["business", "nonprofit", "education"]:
        # Offers they sent
        return [off["id"] for off in SAMPLE_OFFERS if off["brand_id"] == user_id]
    
    if user_type == "agency":
        # Offers for their managed influencers
        managed_ids = set(user.get("managed_influencer_ids", []))
        return [off["id"] for off in SAMPLE_OFFERS if off["influencer_id"] in managed_ids]
    
    if user_type == "influencer":
        # Offers they received
        influencer_id = user_id if user_id.startswith("inf_") else None
        return [off["id"] for off in SAMPLE_OFFERS if off["influencer_id"] == influencer_id]
    
    return []