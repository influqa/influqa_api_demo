/**
 * Influqa API - Authentication Examples (JavaScript)
 * 
 * This file demonstrates how to authenticate with the Influqa API
 * using JavaScript/Node.js
 */

const API_BASE_URL = 'https://api.influqa.com/api/v1';

// ============================================
// 1. User Login
// ============================================
async function login(email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: email,
        password: password
      })
    });

    const data = await response.json();
    
    if (data.success) {
      // Store the JWT token securely
      const token = data.data.token;
      localStorage.setItem('influqa_token', token);
      console.log('Login successful!');
      return token;
    } else {
      console.error('Login failed:', data.error.message);
      return null;
    }
  } catch (error) {
    console.error('Error during login:', error);
    return null;
  }
}

// ============================================
// 2. User Registration
// ============================================
async function register(userData) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        full_name: userData.fullName,
        user_type: userData.userType, // 'influencer', 'brand', 'agency'
        username: userData.username
      })
    });

    const data = await response.json();
    
    if (data.success) {
      console.log('Registration successful!');
      console.log('Please check your email for verification.');
      return data.data;
    } else {
      console.error('Registration failed:', data.error.message);
      return null;
    }
  } catch (error) {
    console.error('Error during registration:', error);
    return null;
  }
}

// ============================================
// 3. Refresh Token
// ============================================
async function refreshToken(currentToken) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${currentToken}`,
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    
    if (data.success) {
      const newToken = data.data.token;
      localStorage.setItem('influqa_token', newToken);
      console.log('Token refreshed successfully!');
      return newToken;
    } else {
      console.error('Token refresh failed:', data.error.message);
      return null;
    }
  } catch (error) {
    console.error('Error refreshing token:', error);
    return null;
  }
}

// ============================================
// 4. Logout
// ============================================
async function logout(token) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/logout`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    
    if (data.success) {
      localStorage.removeItem('influqa_token');
      console.log('Logout successful!');
      return true;
    } else {
      console.error('Logout failed:', data.error.message);
      return false;
    }
  } catch (error) {
    console.error('Error during logout:', error);
    return false;
  }
}

// ============================================
// 5. Google OAuth Login
// ============================================
function redirectToGoogleOAuth() {
  // Redirect user to Google OAuth endpoint
  window.location.href = `${API_BASE_URL}/auth/google`;
}

// Handle Google OAuth callback
async function handleGoogleCallback(code) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/google/callback?code=${code}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    
    if (data.success) {
      localStorage.setItem('influqa_token', data.data.token);
      console.log('Google OAuth login successful!');
      return data.data.token;
    } else {
      console.error('Google OAuth failed:', data.error.message);
      return null;
    }
  } catch (error) {
    console.error('Error during Google OAuth:', error);
    return null;
  }
}

// ============================================
// Helper: Get stored token
// ============================================
function getAuthToken() {
  return localStorage.getItem('influqa_token');
}

// ============================================
// Helper: Make authenticated request
// ============================================
async function makeAuthenticatedRequest(endpoint, options = {}) {
  const token = getAuthToken();
  
  if (!token) {
    throw new Error('No authentication token found');
  }

  const defaultOptions = {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  };

  const mergedOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    }
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, mergedOptions);
  return response.json();
}

// ============================================
// Usage Examples
// ============================================

// Example 1: Login
// login('user@example.com', 'password123');

// Example 2: Register
// register({
//   email: 'newuser@example.com',
//   password: 'securePassword123',
//   fullName: 'John Doe',
//   userType: 'influencer',
//   username: 'johndoe'
// });

// Example 3: Make authenticated request
// makeAuthenticatedRequest('/users/me')
//   .then(data => console.log('User profile:', data))
//   .catch(error => console.error('Error:', error));

module.exports = {
  login,
  register,
  refreshToken,
  logout,
  redirectToGoogleOAuth,
  handleGoogleCallback,
  getAuthToken,
  makeAuthenticatedRequest
};
