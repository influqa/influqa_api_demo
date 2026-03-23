"""
Influqa API - Offers Management Examples (Python)

This file demonstrates offer creation, management, and search operations
using Python with the requests library.

Requirements:
    pip install requests
"""

import requests
from typing import Optional, Dict, Any, List
from auth import InfluqaAuth, API_BASE_URL


class InfluqaOffers:
    """Offers management for Influqa API"""
    
    def __init__(self, auth: InfluqaAuth):
        self.auth = auth
        self.base_url = API_BASE_URL
    
    # ============================================
    # 1. Create Offer
    # ============================================
    def create_offer(self, offer_data: Dict[str, Any]) -> Optional[Dict]:
        """
        Create a new offer.
        
        Args:
            offer_data: Dictionary containing offer information
                - title: Offer title
                - description: Offer description
                - category: Offer category
                - price_usd: Price in USD
                - price_coins: Price in coins (optional)
                - social_media_type: Platform (instagram, tiktok, etc.)
                - followers_count: Follower count
                - deliverables: List of deliverables
                - requirements: List of requirements
                - tags: List of tags
                
        Returns:
            Created offer data or None
        """
        try:
            response = self.auth.request('POST', '/offers', json=offer_data)
            
            if response.get('success'):
                print('Offer created successfully!')
                return response['data']
            else:
                print(f"Failed to create offer: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error creating offer: {e}')
            return None
    
    # ============================================
    # 2. List My Offers
    # ============================================
    def list_my_offers(self, **filters) -> Optional[Dict]:
        """
        List offers created by the authenticated user.
        
        Args:
            status: Filter by status
            category: Filter by category
            page: Page number (default: 1)
            limit: Items per page (default: 20)
            
        Returns:
            List of offers with pagination info
        """
        try:
            params = {k: v for k, v in filters.items() if v is not None}
            response = self.auth.request('GET', '/influencer/offers', params=params)
            
            if response.get('success'):
                return response['data']
            else:
                print(f"Failed to list offers: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error listing offers: {e}')
            return None
    
    # ============================================
    # 3. Get Offer Details
    # ============================================
    def get_offer(self, offer_id: str) -> Optional[Dict]:
        """
        Get detailed information about an offer.
        
        Args:
            offer_id: Unique offer identifier
            
        Returns:
            Offer details or None
        """
        try:
            response = self.auth.request('GET', f'/offers/{offer_id}')
            
            if response.get('success'):
                return response['data']
            else:
                print(f"Failed to get offer: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error fetching offer: {e}')
            return None
    
    # ============================================
    # 4. Update Offer
    # ============================================
    def update_offer(self, offer_id: str, update_data: Dict[str, Any]) -> Optional[Dict]:
        """
        Update an existing offer.
        
        Args:
            offer_id: Offer identifier
            update_data: Fields to update
            
        Returns:
            Updated offer data or None
        """
        try:
            response = self.auth.request('PUT', f'/offers/{offer_id}', json=update_data)
            
            if response.get('success'):
                print('Offer updated successfully!')
                return response['data']
            else:
                print(f"Failed to update offer: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error updating offer: {e}')
            return None
    
    # ============================================
    # 5. Delete Offer
    # ============================================
    def delete_offer(self, offer_id: str) -> bool:
        """
        Delete an offer.
        
        Args:
            offer_id: Offer identifier
            
        Returns:
            True if successful
        """
        try:
            response = self.auth.request('DELETE', f'/offers/{offer_id}')
            
            if response.get('success'):
                print('Offer deleted successfully!')
                return True
            else:
                print(f"Failed to delete offer: {response.get('error', {}).get('message')}")
                return False
                
        except Exception as e:
            print(f'Error deleting offer: {e}')
            return False
    
    # ============================================
    # 6. Search Offers (Public)
    # ============================================
    def search_offers(self, **search_params) -> Optional[Dict]:
        """
        Search for offers with filters.
        
        Args:
            query: Search query string
            category: Filter by category
            min_price: Minimum price
            max_price: Maximum price
            platform: Social media platform
            country: Creator country
            sort: Sort order
            page: Page number
            limit: Items per page
            
        Returns:
            Search results with pagination
        """
        try:
            params = {k: v for k, v in search_params.items() if v is not None}
            
            # Public endpoint - no auth required
            response = requests.get(
                f'{self.base_url}/offers',
                params=params,
                headers={'Content-Type': 'application/json'}
            )
            
            data = response.json()
            
            if data.get('success'):
                return data['data']
            else:
                print(f"Search failed: {data.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error searching offers: {e}')
            return None
    
    # ============================================
    # 7. AI-Powered Search
    # ============================================
    def ai_search(self, query: str) -> Optional[Dict]:
        """
        Search offers using AI-powered natural language search.
        
        Args:
            query: Natural language search query
            
        Returns:
            AI search results
        """
        try:
            response = self.auth.request('POST', '/ai/search', json={'query': query})
            
            if response.get('success'):
                return response['data']
            else:
                print(f"AI search failed: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error in AI search: {e}')
            return None
    
    # ============================================
    # 8. Toggle Offer Status
    # ============================================
    def toggle_status(self, offer_id: str, is_active: bool) -> Optional[Dict]:
        """
        Toggle offer active/paused status.
        
        Args:
            offer_id: Offer identifier
            is_active: True to activate, False to pause
            
        Returns:
            Updated offer data
        """
        try:
            response = self.auth.request(
                'PUT',
                f'/offers/{offer_id}/status',
                json={'is_active': is_active}
            )
            
            if response.get('success'):
                status = 'activated' if is_active else 'paused'
                print(f'Offer {status} successfully!')
                return response['data']
            else:
                print(f"Failed to toggle status: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error toggling status: {e}')
            return None
    
    # ============================================
    # 9. Get Offer by Slug
    # ============================================
    def get_offer_by_slug(self, slug: str) -> Optional[Dict]:
        """
        Get offer by its URL slug.
        
        Args:
            slug: Offer slug
            
        Returns:
            Offer details or None
        """
        try:
            response = requests.get(
                f'{self.base_url}/offers/slug/{slug}',
                headers={'Content-Type': 'application/json'}
            )
            
            data = response.json()
            
            if data.get('success'):
                return data['data']
            else:
                print(f"Failed to get offer: {data.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error fetching offer by slug: {e}')
            return None


# ============================================
# Usage Examples
# ============================================

if __name__ == '__main__':
    from auth import InfluqaAuth
    
    # Initialize auth and login
    auth = InfluqaAuth()
    auth.login('user@example.com', 'password123')
    
    # Initialize offers client
    offers = InfluqaOffers(auth)
    
    # Example 1: Create an offer
    # new_offer = offers.create_offer({
    #     'title': 'Instagram Post - Lifestyle',
    #     'description': 'High-quality lifestyle post on my Instagram account',
    #     'category': 'lifestyle',
    #     'price_usd': 150.00,
    #     'price_coins': 15000,
    #     'social_media_type': 'instagram',
    #     'followers_count': 50000,
    #     'deliverables': [
    #         {'type': 'post', 'quantity': 1, 'description': 'Feed post with photo'},
    #         {'type': 'story', 'quantity': 3, 'description': 'Instagram stories'}
    #     ],
    #     'requirements': [
    #         {'type': 'content', 'description': 'Brand must provide product', 'required': True}
    #     ],
    #     'tags': ['lifestyle', 'fashion', 'instagram']
    # })
    
    # Example 2: Search offers
    # results = offers.search_offers(
    #     query='lifestyle',
    #     category='fashion',
    #     min_price=100,
    #     max_price=500,
    #     platform='instagram',
    #     sort='price_asc',
    #     page=1,
    #     limit=20
    # )
    
    # Example 3: AI search
    # ai_results = offers.ai_search(
    #     'I need a fitness influencer with 50k+ followers for a protein brand'
    # )
    
    # Example 4: List my offers
    # my_offers = offers.list_my_offers(status='active', page=1, limit=10)
    
    pass
