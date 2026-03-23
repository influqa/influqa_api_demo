"""
Basic usage examples for the Influqa API Demo.

This script demonstrates how different user types have access to different resources.
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
        ("demo_key_admin", "admin"),
        ("demo_key_brand", "brand"),
        ("demo_key_agency", "agency"),
        ("demo_key_influencer", "influencer"),
    ]
    
    for api_key, user_type in api_keys:
        response = requests.get(
            f"{BASE_URL}/auth/verify",
            headers={"X-API-Key": api_key}
        )
        
        if response.ok:
            data = response.json()
            print(f"\n✅ {user_type.upper()} - {data['user'].get('company_name') or data['user'].get('username', 'Admin')}")
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
    
    # Admin - should see all influencers
    print("\n--- Admin (Full Access) ---")
    response = requests.get(
        f"{BASE_URL}/influencers",
        headers={"X-API-Key": "demo_key_admin"}
    )
    if response.ok:
        data = response.json()
        print(f"Total influencers visible: {data['count']}")
        print(f"Influencers: {[inf['username'] for inf in data['data']]}")
    
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
    
    # Brand - should see only partnered influencers
    print("\n--- Brand (Partnered Influencers Only) ---")
    response = requests.get(
        f"{BASE_URL}/influencers",
        headers={"X-API-Key": "demo_key_brand"}
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


def test_campaign_access():
    """Test campaign access control."""
    print("\n" + "="*60)
    print("📊 CAMPAIGN ACCESS TESTS")
    print("="*60)
    
    # Admin - should see all campaigns
    print("\n--- Admin (Full Access) ---")
    response = requests.get(
        f"{BASE_URL}/campaigns",
        headers={"X-API-Key": "demo_key_admin"}
    )
    if response.ok:
        data = response.json()
        print(f"Total campaigns visible: {data['count']}")
        print(f"Campaigns: {[camp['title'] for camp in data['data']]}")
    
    # Brand - should see own campaigns only
    print("\n--- Brand (Own Campaigns Only) ---")
    response = requests.get(
        f"{BASE_URL}/campaigns",
        headers={"X-API-Key": "demo_key_brand"}
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
        f"{BASE_URL}/influencers/inf_002",  # Marcus - not the demo influencer
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
        print(f"Result: Empty list ({data['count']} influencers)")
    else:
        print(f"Error: {response.json().get('detail')}")


def test_offers_by_user_type():
    """Test offer visibility by user type."""
    print("\n" + "="*60)
    print("📋 OFFER VISIBILITY TESTS")
    print("="*60)
    
    # Agency - should see offers for their managed influencers
    print("\n--- Agency: Offers for managed influencer (Emma) ---")
    response = requests.get(
        f"{BASE_URL}/influencers/inf_001/offers",
        headers={"X-API-Key": "demo_key_agency"}
    )
    if response.ok:
        data = response.json()
        print(f"Total offers: {data['count']}")
        for offer in data['data']:
            print(f"  - {offer['campaign_title']}: ${offer['amount']} ({offer['status']})")
    
    # Influencer - should see their own offers
    print("\n--- Influencer: Own offers ---")
    response = requests.get(
        f"{BASE_URL}/influencers/inf_001/offers",
        headers={"X-API-Key": "demo_key_influencer"}
    )
    if response.ok:
        data = response.json()
        print(f"Total offers: {data['count']}")


if __name__ == "__main__":
    print("="*60)
    print("🚀 INFLUQA API DEMO - ROLE-BASED ACCESS CONTROL")
    print("="*60)
    print("\nMake sure the server is running: uvicorn main:app --reload")
    print("Then run this script to test the API.")
    
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
        test_offers_by_user_type()
        test_access_denied()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server. Please start the server first:")
        print("   uvicorn main:app --reload")