"""
Basic usage examples for the Influqa API Demo.

This script demonstrates how different user types have access to different resources.
User types from https://www.influqa.com/pricing:
- Influencer
- Business
- Agency
- Nonprofit
- Education
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def print_response(title: str, response: requests.Response):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"📌 {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    if response.ok:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")


def test_auth_verify():
    """Test authentication with different user types."""
    print("\n" + "="*60)
    print("🔐 AUTHENTICATION TESTS")
    print("="*60)
    
    # Test different user types
    api_keys = [
        ("demo_key_influencer", "influencer"),
        ("demo_key_business", "business"),
        ("demo_key_agency", "agency"),
        ("demo_key_nonprofit", "nonprofit"),
        ("demo_key_education", "education"),
    ]
    
    for api_key, user_type in api_keys:
        response = requests.get(
            f"{BASE_URL}/auth/verify",
            headers={"X-API-Key": api_key}
        )
        
        if response.ok:
            data = response.json()
            user_info = data['user']
            print(f"\n✅ {user_type.upper()} - {user_info.get('company_name') or user_info.get('organization_name') or user_info.get('username', 'User')}")
            print(f"   VIP Tier: {user_info.get('vip_tier', 'basic')}")
            print(f"   Accessible influencers: {data['access_summary']['accessible_influencers']}")
            print(f"   Accessible campaigns: {data['access_summary']['accessible_campaigns']}")
            print(f"   Accessible offers: {data['access_summary']['accessible_offers']}")
        else:
            print(f"❌ {user_type}: {response.status_code}")


def test_influencer_access():
    """Test influencer access control."""
    print("\n" + "="*60)
    print("👥 INFLUENCER ACCESS TESTS")
    print("="*60)
    
    # Agency - should see only managed influencers
    print("\n--- Agency (Managed Influencers Only) ---")
    response = requests.get(
        f"{BASE_URL}/influencers",
        headers={"X-API-Key": "demo_key_agency"}
    )
    if response.ok:
        data = response.json()
        print(f"Total influencers visible: {data['count']}")
        print(f"Influencers: {[inf['username'] for inf in data['data']]}")
    
    # Business - should see only partnered influencers
    print("\n--- Business (Partnered Influencers Only) ---")
    response = requests.get(
        f"{BASE_URL}/influencers",
        headers={"X-API-Key": "demo_key_business"}
    )
    if response.ok:
        data = response.json()
        print(f"Total influencers visible: {data['count']}")
        print(f"Influencers: {[inf['username'] for inf in data['data']]}")
    
    # Influencer - should see only own profile
    print("\n--- Influencer (Own Profile Only) ---")
    response = requests.get(
        f"{BASE_URL}/influencers",
        headers={"X-API-Key": "demo_key_influencer"}
    )
    if response.ok:
        data = response.json()
        print(f"Total influencers visible: {data['count']}")
        print(f"Profile: {[inf['username'] for inf in data['data']]}")
    
    # Nonprofit - should see no influencers
    print("\n--- Nonprofit (No Influencer Access) ---")
    response = requests.get(
        f"{BASE_URL}/influencers",
        headers={"X-API-Key": "demo_key_nonprofit"}
    )
    if response.ok:
        data = response.json()
        print(f"Total influencers visible: {data['count']} (no access)")


def test_campaign_access():
    """Test campaign access control."""
    print("\n" + "="*60)
    print("📊 CAMPAIGN ACCESS TESTS")
    print("="*60)
    
    # Business - should see own campaigns only
    print("\n--- Business (Own Campaigns Only) ---")
    response = requests.get(
        f"{BASE_URL}/campaigns",
        headers={"X-API-Key": "demo_key_business"}
    )
    if response.ok:
        data = response.json()
        print(f"Total campaigns visible: {data['count']}")
        print(f"Campaigns: {[camp['title'] for camp in data['data']]}")
    
    # Agency - should see campaigns their influencers are in
    print("\n--- Agency (Campaigns with Managed Influencers) ---")
    response = requests.get(
        f"{BASE_URL}/campaigns",
        headers={"X-API-Key": "demo_key_agency"}
    )
    if response.ok:
        data = response.json()
        print(f"Total campaigns visible: {data['count']}")
        print(f"Campaigns: {[camp['title'] for camp in data['data']]}")
    
    # Influencer - should see campaigns they're hired for
    print("\n--- Influencer (Campaigns Hired For) ---")
    response = requests.get(
        f"{BASE_URL}/campaigns",
        headers={"X-API-Key": "demo_key_influencer"}
    )
    if response.ok:
        data = response.json()
        print(f"Total campaigns visible: {data['count']}")
        print(f"Campaigns: {[camp['title'] for camp in data['data']]}")


def test_access_denied():
    """Test access denied scenarios."""
    print("\n" + "="*60)
    print("🚫 ACCESS DENIED TESTS")
    print("="*60)
    
    # Agency trying to access influencer they don't manage
    print("\n--- Agency accessing non-managed influencer ---")
    response = requests.get(
        f"{BASE_URL}/influencers/inf_003",  # Sophia - not managed by demo agency
        headers={"X-API-Key": "demo_key_agency"}
    )
    print(f"Status: {response.status_code}")
    if not response.ok:
        print(f"Error: {response.json().get('detail')}")
    
    # Influencer trying to access another influencer
    print("\n--- Influencer accessing another influencer's profile ---")
    response = requests.get(
        f"{BASE_URL}/influencers/inf_002",  # Marcus
        headers={"X-API-Key": "demo_key_influencer"}
    )
    print(f"Status: {response.status_code}")
    if not response.ok:
        print(f"Error: {response.json().get('detail')}")
    
    # Nonprofit trying to access influencers
    print("\n--- Nonprofit trying to list influencers ---")
    response = requests.get(
        f"{BASE_URL}/influencers",
        headers={"X-API-Key": "demo_key_nonprofit"}
    )
    if response.ok:
        data = response.json()
        print(f"Result: Empty list ({data['count']} influencers) - no access")


def test_vip_tier_info():
    """Test VIP tier information."""
    print("\n" + "="*60)
    print("💎 VIP TIER INFORMATION")
    print("="*60)
    
    print("\nVIP Tiers available:")
    print("  Basic  - FREE      - Limited API access")
    print("  SVIP   - $4.99/mo  - Enhanced features")
    print("  GVIP   - $19.99/mo - Full platform access")
    
    print("\nDemo user VIP tiers:")
    demo_users = [
        ("demo_key_influencer", "Influencer", "SVIP"),
        ("demo_key_business", "Business", "GVIP"),
        ("demo_key_agency", "Agency", "GVIP"),
        ("demo_key_nonprofit", "Nonprofit", "SVIP"),
        ("demo_key_education", "Education", "Basic"),
    ]
    
    for key, user_type, expected_tier in demo_users:
        response = requests.get(
            f"{BASE_URL}/auth/verify",
            headers={"X-API-Key": key}
        )
        if response.ok:
            actual_tier = response.json()['user'].get('vip_tier', 'basic')
            status = "✅" if actual_tier == expected_tier.lower() else "❌"
            print(f"  {status} {user_type}: {actual_tier.upper()}")


if __name__ == "__main__":
    print("="*60)
    print("🚀 INFLUQA API DEMO - ROLE-BASED ACCESS CONTROL")
    print("="*60)
    print("\nUser Types: Influencer, Business, Agency, Nonprofit, Education")
    print("VIP Tiers: Basic (FREE), SVIP ($4.99/mo), GVIP ($19.99/mo)")
    print("\nMake sure the server is running: uvicorn main:app --reload")
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/health")
        if not response.ok:
            print("\n❌ Server is not responding. Please start the server first.")
            exit(1)
        
        # Run tests
        test_auth_verify()
        test_influencer_access()
        test_campaign_access()
        test_vip_tier_info()
        test_access_denied()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server. Please start the server first:")
        print("   uvicorn main:app --reload")