"""
Influqa API Demo – Campaign Workflow Example
=============================================
This script demonstrates a complete campaign workflow:
  1. Create a new campaign
  2. Search for matching influencers
  3. Activate the campaign
  4. Check campaign analytics
  5. Get an account overview

Usage:
    python examples/campaign_workflow.py
"""

import httpx
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"
API_KEY = "demo_key_brand"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def create_campaign():
    print("\n=== 1. Create Campaign ===")
    payload = {
        "title": "Back-to-School Tech Accessories 2025",
        "description": (
            "Promote our new line of laptop bags and tech accessories "
            "targeting students and young professionals."
        ),
        "niche": "technology",
        "platforms": ["instagram", "youtube"],
        "budget": 12000,
        "currency": "USD",
        "influencer_requirements": {
            "min_followers": 50000,
            "max_followers": 600000,
            "min_engagement_rate": 4.0,
            "required_niches": ["technology", "lifestyle"],
            "preferred_locations": ["US", "CA", "UK"],
        },
        "deliverables": [
            {"type": "feed_post", "count": 2},
            {"type": "story", "count": 4},
            {"type": "video_review", "count": 1},
        ],
        "start_date": str(date.today() + timedelta(days=7)),
        "end_date": str(date.today() + timedelta(days=37)),
    }
    response = httpx.post(f"{BASE_URL}/campaigns", headers=HEADERS, json=payload)
    response.raise_for_status()
    campaign = response.json()
    print(f"Created campaign: {campaign['title']}")
    print(f"Campaign ID:      {campaign['id']}")
    print(f"Status:           {campaign['status']}")
    print(f"Budget:           ${campaign['budget']:,.2f}")
    print(f"Duration:         {campaign['start_date']} → {campaign['end_date']}")
    return campaign


def find_matching_influencers(campaign: dict):
    print("\n=== 2. Find Matching Influencers ===")
    req = campaign["influencer_requirements"]
    params = {
        "niche": campaign["niche"],
        "min_followers": req["min_followers"],
        "min_engagement_rate": req["min_engagement_rate"],
        "verified_only": True,
    }
    response = httpx.get(f"{BASE_URL}/influencers", headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    print(f"Found {data['total']} matching influencer(s):")
    for inf in data["influencers"]:
        print(
            f"  • {inf['full_name']} (@{inf['username']}) – "
            f"{inf['follower_count']:,} followers, "
            f"{inf['engagement_rate']}% engagement rate, "
            f"${inf['rate_per_post']}/post"
        )
    return data


def activate_campaign(campaign_id: str):
    print(f"\n=== 3. Activate Campaign ===")
    response = httpx.patch(
        f"{BASE_URL}/campaigns/{campaign_id}/status",
        headers=HEADERS,
        params={"status": "active"},
    )
    response.raise_for_status()
    campaign = response.json()
    print(f"Campaign '{campaign['title']}' is now: {campaign['status'].upper()}")
    return campaign


def check_analytics(campaign_id: str):
    print(f"\n=== 4. Campaign Analytics (camp_001 – sample data) ===")
    response = httpx.get(f"{BASE_URL}/analytics/campaigns/camp_001", headers=HEADERS)
    response.raise_for_status()
    a = response.json()
    print(f"Total Reach:       {a['total_reach']:,}")
    print(f"Total Impressions: {a['total_impressions']:,}")
    print(f"Total Engagements: {a['total_engagements']:,}")
    print(f"Engagement Rate:   {a['engagement_rate']}%")
    print(f"Total Clicks:      {a['total_clicks']:,}")
    print(f"Total Conversions: {a['total_conversions']:,}")
    print(f"ROI:               {a['roi']}%")
    print(f"Cost per Click:    ${a['cost_per_click']}")
    print(f"Cost per Conv.:    ${a['cost_per_conversion']}")
    print(f"\nInfluencer Performance:")
    for perf in a["influencer_performance"]:
        print(
            f"  • {perf['influencer_id']}: "
            f"reach={perf['reach']:,}, "
            f"engagements={perf['engagements']:,}, "
            f"conversions={perf['conversions']}"
        )
    return a


def account_overview():
    print("\n=== 5. Account Overview ===")
    response = httpx.get(f"{BASE_URL}/analytics/overview", headers=HEADERS)
    response.raise_for_status()
    ov = response.json()
    print(f"Total Campaigns:    {ov['total_campaigns']}")
    print(f"Active Campaigns:   {ov['active_campaigns']}")
    print(f"Completed:          {ov['completed_campaigns']}")
    print(f"Total Reach:        {ov['total_reach']:,}")
    print(f"Total Impressions:  {ov['total_impressions']:,}")
    print(f"Avg. Engagement:    {ov['average_engagement_rate']}%")
    print(f"Total Conversions:  {ov['total_conversions']:,}")
    print(f"Average ROI:        {ov['average_roi']}%")
    return ov


if __name__ == "__main__":
    try:
        campaign = create_campaign()
        find_matching_influencers(campaign)
        activate_campaign(campaign["id"])
        check_analytics(campaign["id"])
        account_overview()
        print("\n✅ Campaign workflow completed successfully!")
    except httpx.ConnectError:
        print(
            "\n❌ Could not connect to the API server.\n"
            "   Start the server first: uvicorn main:app --reload"
        )
    except httpx.HTTPStatusError as e:
        print(f"\n❌ HTTP Error: {e.response.status_code} – {e.response.text}")
