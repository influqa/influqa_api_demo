"""
Influqa API - Authentication Examples (Python)

This file demonstrates how to authenticate with the Influqa API
using Python with the requests library.

Requirements:
    pip install requests
"""

import requests
import json
from typing import Optional, Dict, Any

API_BASE_URL = 'https://api.influqa.com/api/v1'


class InfluqaAuth:
    """Authentication handler for Influqa API"""
    
    def __init__(self):
        self.token: Optional[str] = None
        self.base_url = API_BASE_URL
    
    # ============================================
    # 1. User Login
    # ============================================
    def login(self, email: str, password: str) -> Optional[str]:
        """
        Authenticate user and store JWT token.
        
        Args:
            email: User email address
            password: User password
            
        Returns:
            JWT token string or None if failed
        """
        try:
            response = requests.post(
                f'{self.base_url}/auth/login',
                json={'email': email, 'password': password}
            )
            
            data = response.json()
            
            if data.get('success'):
                self.token = data['data']['token']
                print('Login successful!')
                return self.token
            else:
                print(f"Login failed: {data.get('error', {}).get('message')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f'Error during login: {e}')
            return None
    
    # ============================================
    # 2. User Registration
    # ============================================
    def register(self, user_data: Dict[str, Any]) -> Optional[Dict]:
        """
        Register a new user account.
        
        Args:
            user_data: Dictionary containing user information
                - email: User email
                - password: User password
                - full_name: Full name
                - user_type: 'influencer', 'brand', or 'agency'
                - username: Unique username
                
        Returns:
            User data dict or None if failed
        """
        try:
            response = requests.post(
                f'{self.base_url}/auth/register',
                json={
                    'email': user_data['email'],
                    'password': user_data['password'],
                    'full_name': user_data['full_name'],
                    'user_type': user_data['user_type'],
                    'username': user_data['username']
                }
            )
            
            data = response.json()
            
            if data.get('success'):
                print('Registration successful!')
                print('Please check your email for verification.')
                return data['data']
            else:
                print(f"Registration failed: {data.get('error', {}).get('message')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f'Error during registration: {e}')
            return None
    
    # ============================================
    # 3. Refresh Token
    # ============================================
    def refresh_token(self) -> Optional[str]:
        """
        Refresh the current JWT token.
        
        Returns:
            New JWT token string or None if failed
        """
        if not self.token:
            print('No token to refresh')
            return None
            
        try:
            response = requests.post(
                f'{self.base_url}/auth/refresh',
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            data = response.json()
            
            if data.get('success'):
                self.token = data['data']['token']
                print('Token refreshed successfully!')
                return self.token
            else:
                print(f"Token refresh failed: {data.get('error', {}).get('message')}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f'Error refreshing token: {e}')
            return None
    
    # ============================================
    # 4. Logout
    # ============================================
    def logout(self) -> bool:
        """
        Logout user and invalidate token.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.token:
            print('No active session')
            return True
            
        try:
            response = requests.post(
                f'{self.base_url}/auth/logout',
                headers={'Authorization': f'Bearer {self.token}'}
            )
            
            data = response.json()
            
            if data.get('success'):
                self.token = None
                print('Logout successful!')
                return True
            else:
                print(f"Logout failed: {data.get('error', {}).get('message')}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f'Error during logout: {e}')
            return False
    
    # ============================================
    # 5. Get Auth Headers
    # ============================================
    def get_headers(self) -> Dict[str, str]:
        """
        Get headers with authentication token.
        
        Returns:
            Dictionary with Authorization header
        """
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    # ============================================
    # 6. Make Authenticated Request
    # ============================================
    def request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make an authenticated API request.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
            
        Returns:
            Response data dictionary
        """
        if not self.token:
            raise Exception('No authentication token. Please login first.')
        
        url = f'{self.base_url}{endpoint}'
        headers = self.get_headers()
        
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                **{k: v for k, v in kwargs.items() if k != 'headers'}
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f'API request failed: {e}')
            raise


# ============================================
# Usage Examples
# ============================================

if __name__ == '__main__':
    auth = InfluqaAuth()
    
    # Example 1: Login
    # token = auth.login('user@example.com', 'password123')
    
    # Example 2: Register
    # user_data = {
    #     'email': 'newuser@example.com',
    #     'password': 'securePassword123',
    #     'full_name': 'John Doe',
    #     'user_type': 'influencer',
    #     'username': 'johndoe'
    # }
    # auth.register(user_data)
    
    # Example 3: Make authenticated request
    # auth.login('user@example.com', 'password123')
    # response = auth.request('GET', '/users/me')
    # print(response)
    
    # Example 4: Logout
    # auth.logout()
    pass
