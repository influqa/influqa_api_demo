/**
 * Influqa API - User Management Examples (JavaScript)
 * 
 * This file demonstrates user profile and management operations
 */

const API_BASE_URL = 'https://api.influqa.com/api/v1';

// ============================================
// Helper: Get auth token from storage
// ============================================
function getAuthToken() {
  return localStorage.getItem('influqa_token');
}

// ============================================
// Helper: Make authenticated request
// ============================================
async function apiRequest(endpoint, options = {}) {
  const token = getAuthToken();
  
  const defaultOptions = {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers
    }
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

// ============================================
// 1. Get Current User Profile
// ============================================
async function getCurrentUser() {
  try {
    const data = await apiRequest('/users/me');
    console.log('Current user:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching user:', error);
    throw error;
  }
}

// ============================================
// 2. Update User Profile
// ============================================
async function updateProfile(profileData) {
  try {
    const data = await apiRequest('/users/me', {
      method: 'PUT',
      body: JSON.stringify({
        full_name: profileData.fullName,
        bio: profileData.bio,
        country: profileData.country,
        city: profileData.city,
        website: profileData.website,
        social_links: profileData.socialLinks,
        category: profileData.category
      })
    });
    console.log('Profile updated:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error updating profile:', error);
    throw error;
  }
}

// ============================================
// 3. Upload Profile Image
// ============================================
async function uploadProfileImage(imageFile) {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);

    const token = getAuthToken();
    const response = await fetch(`${API_BASE_URL}/users/me/avatar`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    const data = await response.json();
    console.log('Avatar uploaded:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error uploading avatar:', error);
    throw error;
  }
}

// ============================================
// 4. Get User by Username (Public Profile)
// ============================================
async function getPublicProfile(username) {
  try {
    // Public endpoint - no auth required
    const response = await fetch(`${API_BASE_URL}/users/${username}`, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();
    console.log('Public profile:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching public profile:', error);
    throw error;
  }
}

// ============================================
// 5. List All Users (Admin only)
// ============================================
async function listUsers(filters = {}) {
  try {
    const queryParams = new URLSearchParams();
    
    if (filters.type) queryParams.append('type', filters.type);
    if (filters.status) queryParams.append('status', filters.status);
    if (filters.vip_tier) queryParams.append('vip_tier', filters.vip_tier);
    if (filters.search) queryParams.append('search', filters.search);
    if (filters.page) queryParams.append('page', filters.page.toString());
    if (filters.limit) queryParams.append('limit', filters.limit.toString());
    if (filters.sort) queryParams.append('sort', filters.sort);
    if (filters.order) queryParams.append('order', filters.order);

    const data = await apiRequest(`/admin/users?${queryParams.toString()}`);
    console.log('Users list:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error listing users:', error);
    throw error;
  }
}

// ============================================
// 6. Get User Details (Admin only)
// ============================================
async function getUserDetails(userId) {
  try {
    const data = await apiRequest(`/admin/users/${userId}`);
    console.log('User details:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching user details:', error);
    throw error;
  }
}

// ============================================
// 7. Ban User (Admin only)
// ============================================
async function banUser(userId, reason) {
  try {
    const data = await apiRequest(`/admin/users/${userId}/ban`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    });
    console.log('User banned:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error banning user:', error);
    throw error;
  }
}

// ============================================
// 8. Verify User (Admin only)
// ============================================
async function verifyUser(userId) {
  try {
    const data = await apiRequest(`/admin/users/${userId}/verify`, {
      method: 'POST'
    });
    console.log('User verified:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error verifying user:', error);
    throw error;
  }
}

// ============================================
// 9. Change Password
// ============================================
async function changePassword(currentPassword, newPassword) {
  try {
    const data = await apiRequest('/users/me/password', {
      method: 'PUT',
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword
      })
    });
    console.log('Password changed successfully');
    return data.data;
  } catch (error) {
    console.error('Error changing password:', error);
    throw error;
  }
}

// ============================================
// 10. Update Email
// ============================================
async function updateEmail(newEmail, password) {
  try {
    const data = await apiRequest('/users/me/email', {
      method: 'PUT',
      body: JSON.stringify({
        email: newEmail,
        password: password
      })
    });
    console.log('Email update requested. Check your new email for verification.');
    return data.data;
  } catch (error) {
    console.error('Error updating email:', error);
    throw error;
  }
}

// ============================================
// 11. Delete Account
// ============================================
async function deleteAccount(password) {
  try {
    const data = await apiRequest('/users/me', {
      method: 'DELETE',
      body: JSON.stringify({ password })
    });
    console.log('Account deleted successfully');
    localStorage.removeItem('influqa_token');
    return data.data;
  } catch (error) {
    console.error('Error deleting account:', error);
    throw error;
  }
}

// ============================================
// Usage Examples
// ============================================

// Example 1: Get current user
// getCurrentUser().then(user => console.log(user));

// Example 2: Update profile
// updateProfile({
//   fullName: 'John Updated',
//   bio: 'Professional influencer and content creator',
//   country: 'US',
//   city: 'New York',
//   category: 'lifestyle'
// });

// Example 3: List users with filters (Admin)
// listUsers({
//   type: 'influencer',
//   status: 'active',
//   page: 1,
//   limit: 20
// });

// Example 4: Get public profile
// getPublicProfile('johndoe');

module.exports = {
  getCurrentUser,
  updateProfile,
  uploadProfileImage,
  getPublicProfile,
  listUsers,
  getUserDetails,
  banUser,
  verifyUser,
  changePassword,
  updateEmail,
  deleteAccount
};
