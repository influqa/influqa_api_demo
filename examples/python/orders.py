"""
Influqa API - Orders Management Examples (Python)

This file demonstrates order creation, management, and tracking operations
using Python with the requests library.

Requirements:
    pip install requests
"""

import requests
from typing import Optional, Dict, Any, List
from auth import InfluqaAuth, API_BASE_URL


class InfluqaOrders:
    """Orders management for Influqa API"""
    
    def __init__(self, auth: InfluqaAuth):
        self.auth = auth
        self.base_url = API_BASE_URL
    
    # ============================================
    # 1. Create Order
    # ============================================
    def create_order(self, order_data: Dict[str, Any]) -> Optional[Dict]:
        """
        Create a new order for an offer.
        
        Args:
            order_data: Dictionary containing order information
                - offer_id: ID of the offer to purchase
                - requirements: Requirements for the order
                - message: Message to the seller
                - payment_method: 'stripe' or 'coins'
                - use_coins: Whether to use coins for payment
                - coins_amount: Amount of coins to use
                
        Returns:
            Created order data or None
        """
        try:
            response = self.auth.request('POST', '/orders', json=order_data)
            
            if response.get('success'):
                print('Order created successfully!')
                return response['data']
            else:
                print(f"Failed to create order: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error creating order: {e}')
            return None
    
    # ============================================
    # 2. Get Order Details
    # ============================================
    def get_order(self, order_id: str) -> Optional[Dict]:
        """
        Get detailed information about an order.
        
        Args:
            order_id: Unique order identifier
            
        Returns:
            Order details or None
        """
        try:
            response = self.auth.request('GET', f'/orders/{order_id}')
            
            if response.get('success'):
                return response['data']
            else:
                print(f"Failed to get order: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error fetching order: {e}')
            return None
    
    # ============================================
    # 3. List My Orders (as Buyer)
    # ============================================
    def list_my_orders(self, **filters) -> Optional[Dict]:
        """
        List orders placed by the authenticated user.
        
        Args:
            status: Filter by status
            page: Page number
            limit: Items per page
            sort: Sort order
            
        Returns:
            List of orders with pagination
        """
        try:
            params = {k: v for k, v in filters.items() if v is not None}
            response = self.auth.request('GET', '/orders', params=params)
            
            if response.get('success'):
                return response['data']
            else:
                print(f"Failed to list orders: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error listing orders: {e}')
            return None
    
    # ============================================
    # 4. List Orders as Seller
    # ============================================
    def list_seller_orders(self, **filters) -> Optional[Dict]:
        """
        List orders received by the authenticated seller.
        
        Args:
            status: Filter by status
            page: Page number
            limit: Items per page
            
        Returns:
            List of orders with pagination
        """
        try:
            params = {k: v for k, v in filters.items() if v is not None}
            response = self.auth.request('GET', '/influencer/orders', params=params)
            
            if response.get('success'):
                return response['data']
            else:
                print(f"Failed to list seller orders: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error listing seller orders: {e}')
            return None
    
    # ============================================
    # 5. Accept Order (Seller)
    # ============================================
    def accept_order(self, order_id: str) -> Optional[Dict]:
        """
        Accept a pending order as seller.
        
        Args:
            order_id: Order identifier
            
        Returns:
            Updated order data
        """
        try:
            response = self.auth.request('POST', f'/orders/{order_id}/accept')
            
            if response.get('success'):
                print('Order accepted successfully!')
                return response['data']
            else:
                print(f"Failed to accept order: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error accepting order: {e}')
            return None
    
    # ============================================
    # 6. Reject Order (Seller)
    # ============================================
    def reject_order(self, order_id: str, reason: str) -> Optional[Dict]:
        """
        Reject a pending order as seller.
        
        Args:
            order_id: Order identifier
            reason: Reason for rejection
            
        Returns:
            Updated order data
        """
        try:
            response = self.auth.request(
                'POST',
                f'/orders/{order_id}/reject',
                json={'reason': reason}
            )
            
            if response.get('success'):
                print('Order rejected successfully!')
                return response['data']
            else:
                print(f"Failed to reject order: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error rejecting order: {e}')
            return None
    
    # ============================================
    # 7. Start Order (Seller)
    # ============================================
    def start_order(self, order_id: str) -> Optional[Dict]:
        """
        Mark order as in progress.
        
        Args:
            order_id: Order identifier
            
        Returns:
            Updated order data
        """
        try:
            response = self.auth.request('POST', f'/orders/{order_id}/start')
            
            if response.get('success'):
                print('Order started successfully!')
                return response['data']
            else:
                print(f"Failed to start order: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error starting order: {e}')
            return None
    
    # ============================================
    # 8. Deliver Order (Seller)
    # ============================================
    def deliver_order(self, order_id: str, delivery_data: Dict[str, Any]) -> Optional[Dict]:
        """
        Deliver completed work for an order.
        
        Args:
            order_id: Order identifier
            delivery_data: Dictionary containing
                - message: Delivery message
                - attachments: List of attachment URLs
                - links: List of relevant links
            
        Returns:
            Updated order data
        """
        try:
            response = self.auth.request(
                'POST',
                f'/orders/{order_id}/deliver',
                json=delivery_data
            )
            
            if response.get('success'):
                print('Order delivered successfully!')
                return response['data']
            else:
                print(f"Failed to deliver order: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error delivering order: {e}')
            return None
    
    # ============================================
    # 9. Request Revision (Buyer)
    # ============================================
    def request_revision(self, order_id: str, revision_data: Dict[str, Any]) -> Optional[Dict]:
        """
        Request revision for delivered work.
        
        Args:
            order_id: Order identifier
            revision_data: Dictionary containing
                - message: Revision request message
                - requirements: Additional requirements
            
        Returns:
            Updated order data
        """
        try:
            response = self.auth.request(
                'POST',
                f'/orders/{order_id}/revision',
                json=revision_data
            )
            
            if response.get('success'):
                print('Revision requested successfully!')
                return response['data']
            else:
                print(f"Failed to request revision: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error requesting revision: {e}')
            return None
    
    # ============================================
    # 10. Complete Order (Buyer)
    # ============================================
    def complete_order(self, order_id: str) -> Optional[Dict]:
        """
        Mark order as complete and release payment.
        
        Args:
            order_id: Order identifier
            
        Returns:
            Updated order data
        """
        try:
            response = self.auth.request('POST', f'/orders/{order_id}/complete')
            
            if response.get('success'):
                print('Order completed successfully!')
                return response['data']
            else:
                print(f"Failed to complete order: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error completing order: {e}')
            return None
    
    # ============================================
    # 11. Cancel Order
    # ============================================
    def cancel_order(self, order_id: str, reason: str) -> Optional[Dict]:
        """
        Cancel an order.
        
        Args:
            order_id: Order identifier
            reason: Cancellation reason
            
        Returns:
            Updated order data
        """
        try:
            response = self.auth.request(
                'POST',
                f'/orders/{order_id}/cancel',
                json={'reason': reason}
            )
            
            if response.get('success'):
                print('Order cancelled successfully!')
                return response['data']
            else:
                print(f"Failed to cancel order: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error cancelling order: {e}')
            return None
    
    # ============================================
    # 12. Get Order Messages
    # ============================================
    def get_messages(self, order_id: str) -> Optional[List[Dict]]:
        """
        Get messages for an order.
        
        Args:
            order_id: Order identifier
            
        Returns:
            List of messages
        """
        try:
            response = self.auth.request('GET', f'/orders/{order_id}/messages')
            
            if response.get('success'):
                return response['data']
            else:
                print(f"Failed to get messages: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error fetching messages: {e}')
            return None
    
    # ============================================
    # 13. Send Order Message
    # ============================================
    def send_message(self, order_id: str, message: str, attachments: List[str] = None) -> Optional[Dict]:
        """
        Send a message in an order.
        
        Args:
            order_id: Order identifier
            message: Message text
            attachments: List of attachment URLs
            
        Returns:
            Sent message data
        """
        try:
            payload = {'message': message}
            if attachments:
                payload['attachments'] = attachments
                
            response = self.auth.request(
                'POST',
                f'/orders/{order_id}/messages',
                json=payload
            )
            
            if response.get('success'):
                print('Message sent successfully!')
                return response['data']
            else:
                print(f"Failed to send message: {response.get('error', {}).get('message')}")
                return None
                
        except Exception as e:
            print(f'Error sending message: {e}')
            return None


# ============================================
# Usage Examples
# ============================================

if __name__ == '__main__':
    from auth import InfluqaAuth
    
    # Initialize auth and login
    auth = InfluqaAuth()
    auth.login('user@example.com', 'password123')
    
    # Initialize orders client
    orders = InfluqaOrders(auth)
    
    # Example 1: Create an order
    # new_order = orders.create_order({
    #     'offer_id': 'offer_123456',
    #     'requirements': 'Please create a post featuring our new product',
    #     'message': 'Looking forward to working with you!',
    #     'payment_method': 'stripe',
    #     'use_coins': False
    # })
    
    # Example 2: Accept order (as seller)
    # orders.accept_order('order_789012')
    
    # Example 3: Deliver order
    # orders.deliver_order('order_789012', {
    #     'message': 'Here is the completed work!',
    #     'attachments': ['https://example.com/image1.jpg'],
    #     'links': ['https://instagram.com/p/ABC123']
    # })
    
    # Example 4: Complete order (as buyer)
    # orders.complete_order('order_789012')
    
    pass
