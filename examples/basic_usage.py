"""
Influqa API Demo – Basic Usage Examples
========================================
This script demonstrates the basic usage of the Influqa API:
  1. Verifying your API key
  2. Searching for influencers
  3. Retrieving a specific influencer profile

Usage:
    python examples/basic_usage.py
"""

import httpx

BASE_URL = "http://localhost:8000"
API_KEY = "demo_key_brand"
HEADERS = {"X-API-Key": API_KEY}


def verify_api_key():
    print("\n=== 1. Verify API Key ===")
    response = httpx.get(f"{BASE_URL}/auth/verify", headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    print(f"Authenticated as: {data['company_name']} ({data['role']})")
    return data


def search_influencers():
    print("\n=== 2. Search Influencers ===")
    params = {
        "platform": "instagram",
        "min_followers": 100000,
        "min_engagement_rate": 4.0,
        "verified_only": True,
    }
    response = httpx.get(f"{BASE_URL}/influencers", headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()
    print(f"Found {data['total']} influencers matching your criteria:")
    for inf in data["influencers"]:
        print(
            f"  • {inf['full_name']} (@{inf['username']}) – "
            f"{inf['follower_count']:,} followers, "
            f"{inf['engagement_rate']}% engagement, "
            f"${inf['rate_per_post']}/post"
        )
    return data


def get_influencer_profile(influencer_id: str):
    print(f"\n=== 3. Get Influencer Profile: {influencer_id} ===")
    response = httpx.get(f"{BASE_URL}/influencers/{influencer_id}", headers=HEADERS)
    response.raise_for_status()
    inf = response.json()
    print(f"Name:        {inf['full_name']}")
    print(f"Platform:    {inf['platform'].capitalize()}")
    print(f"Niche:       {inf['niche'].capitalize()}")
    print(f"Followers:   {inf['follower_count']:,}")
    print(f"Engagement:  {inf['engagement_rate']}%")
    print(f"Rate/post:   ${inf['rate_per_post']}")
    print(f"Location:    {inf['location']}")
    print(f"Tags:        {', '.join(inf['tags'])}")
    demo = inf["audience_demographics"]
    print(f"Audience:    {demo['female']}% female, {demo['male']}% male")
    print(f"Top markets: {', '.join(demo['top_countries'])}")
    return inf


def search_by_niche(niche: str):
    print(f"\n=== 4. Search by Niche: {niche} ===")
    response = httpx.get(
        f"{BASE_URL}/influencers", headers=HEADERS, params={"niche": niche}
    )
    response.raise_for_status()
    data = response.json()
    print(f"Found {data['total']} {niche} influencers:")
    for inf in data["influencers"]:
        print(f"  • {inf['full_name']} – {inf['follower_count']:,} followers")
    return data


if __name__ == "__main__":
    try:
        user = verify_api_key()
        results = search_influencers()
        if results["influencers"]:
            first_id = results["influencers"][0]["id"]
            get_influencer_profile(first_id)
        search_by_niche("fitness")
        print("\n✅ All examples completed successfully!")
    except httpx.ConnectError:
        print(
            "\n❌ Could not connect to the API server.\n"
            "   Start the server first: uvicorn main:app --reload"
        )
    except httpx.HTTPStatusError as e:
        print(f"\n❌ HTTP Error: {e.response.status_code} – {e.response.text}")
