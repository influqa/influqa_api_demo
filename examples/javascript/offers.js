/**
 * Influqa API - Offers Management Examples (JavaScript)
 * 
 * This file demonstrates offer creation, management, and search operations
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
// 1. Create Offer
// ============================================
async function createOffer(offerData) {
  try {
    const data = await apiRequest('/offers', {
      method: 'POST',
      body: JSON.stringify({
        title: offerData.title,
        description: offerData.description,
        category: offerData.category,
        price_usd: offerData.priceUsd,
        price_coins: offerData.priceCoins,
        social_media_type: offerData.socialMediaType, // 'instagram', 'tiktok', etc.
        followers_count: offerData.followersCount,
        deliverables: offerData.deliverables || [],
        requirements: offerData.requirements || [],
        tags: offerData.tags || [],
        images: offerData.images || []
      })
    });
    console.log('Offer created:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error creating offer:', error);
    throw error;
  }
}

// ============================================
// 2. List My Offers (as Influencer)
// ============================================
async function listMyOffers(filters = {}) {
  try {
    const queryParams = new URLSearchParams();
    
    if (filters.status) queryParams.append('status', filters.status);
    if (filters.category) queryParams.append('category', filters.category);
    if (filters.page) queryParams.append('page', filters.page.toString());
    if (filters.limit) queryParams.append('limit', filters.limit.toString());

    const data = await apiRequest(`/influencer/offers?${queryParams.toString()}`);
    console.log('My offers:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error listing offers:', error);
    throw error;
  }
}

// ============================================
// 3. Get Offer Details
// ============================================
async function getOffer(offerId) {
  try {
    const data = await apiRequest(`/offers/${offerId}`);
    console.log('Offer details:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching offer:', error);
    throw error;
  }
}

// ============================================
// 4. Update Offer
// ============================================
async function updateOffer(offerId, updateData) {
  try {
    const data = await apiRequest(`/offers/${offerId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData)
    });
    console.log('Offer updated:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error updating offer:', error);
    throw error;
  }
}

// ============================================
// 5. Delete Offer
// ============================================
async function deleteOffer(offerId) {
  try {
    const data = await apiRequest(`/offers/${offerId}`, {
      method: 'DELETE'
    });
    console.log('Offer deleted:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error deleting offer:', error);
    throw error;
  }
}

// ============================================
// 6. Search Offers (Public)
// ============================================
async function searchOffers(searchParams = {}) {
  try {
    const queryParams = new URLSearchParams();
    
    if (searchParams.query) queryParams.append('q', searchParams.query);
    if (searchParams.category) queryParams.append('category', searchParams.category);
    if (searchParams.minPrice) queryParams.append('min_price', searchParams.minPrice.toString());
    if (searchParams.maxPrice) queryParams.append('max_price', searchParams.maxPrice.toString());
    if (searchParams.platform) queryParams.append('platform', searchParams.platform);
    if (searchParams.country) queryParams.append('country', searchParams.country);
    if (searchParams.sort) queryParams.append('sort', searchParams.sort);
    if (searchParams.page) queryParams.append('page', searchParams.page.toString());
    if (searchParams.limit) queryParams.append('limit', searchParams.limit.toString());

    // Public endpoint - no auth required
    const response = await fetch(`${API_BASE_URL}/offers?${queryParams.toString()}`, {
      headers: { 'Content-Type': 'application/json' }
    });

    const data = await response.json();
    console.log('Search results:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error searching offers:', error);
    throw error;
  }
}

// ============================================
// 7. AI-Powered Offer Search
// ============================================
async function aiSearchOffers(query) {
  try {
    const data = await apiRequest('/ai/search', {
      method: 'POST',
      body: JSON.stringify({ query })
    });
    console.log('AI search results:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error in AI search:', error);
    throw error;
  }
}

// ============================================
// 8. Get Offer by Slug (Public)
// ============================================
async function getOfferBySlug(slug) {
  try {
    const response = await fetch(`${API_BASE_URL}/offers/slug/${slug}`, {
      headers: { 'Content-Type': 'application/json' }
    });

    const data = await response.json();
    console.log('Offer by slug:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching offer by slug:', error);
    throw error;
  }
}

// ============================================
// 9. Toggle Offer Status (Active/Paused)
// ============================================
async function toggleOfferStatus(offerId, isActive) {
  try {
    const data = await apiRequest(`/offers/${offerId}/status`, {
      method: 'PUT',
      body: JSON.stringify({ is_active: isActive })
    });
    console.log('Offer status updated:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error toggling offer status:', error);
    throw error;
  }
}

// ============================================
// 10. Upload Offer Images
// ============================================
async function uploadOfferImages(offerId, imageFiles) {
  try {
    const formData = new FormData();
    imageFiles.forEach((file, index) => {
      formData.append(`image_${index}`, file);
    });

    const token = getAuthToken();
    const response = await fetch(`${API_BASE_URL}/offers/${offerId}/images`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    });

    const data = await response.json();
    console.log('Images uploaded:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error uploading images:', error);
    throw error;
  }
}

// ============================================
// 11. Admin: List All Offers
// ============================================
async function adminListOffers(filters = {}) {
  try {
    const queryParams = new URLSearchParams();
    
    if (filters.status) queryParams.append('status', filters.status);
    if (filters.category) queryParams.append('category', filters.category);
    if (filters.search) queryParams.append('search', filters.search);
    if (filters.page) queryParams.append('page', filters.page.toString());
    if (filters.limit) queryParams.append('limit', filters.limit.toString());

    const data = await apiRequest(`/admin/offers?${queryParams.toString()}`);
    console.log('Admin offers list:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error listing admin offers:', error);
    throw error;
  }
}

// ============================================
// 12. Admin: Approve Offer
// ============================================
async function adminApproveOffer(offerId) {
  try {
    const data = await apiRequest(`/admin/offers/${offerId}/approve`, {
      method: 'POST'
    });
    console.log('Offer approved:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error approving offer:', error);
    throw error;
  }
}

// ============================================
// 13. Admin: Reject Offer
// ============================================
async function adminRejectOffer(offerId, reason) {
  try {
    const data = await apiRequest(`/admin/offers/${offerId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    });
    console.log('Offer rejected:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error rejecting offer:', error);
    throw error;
  }
}

// ============================================
// 14. Admin: Feature Offer
// ============================================
async function adminFeatureOffer(offerId, featured = true) {
  try {
    const data = await apiRequest(`/admin/offers/${offerId}/feature`, {
      method: 'POST',
      body: JSON.stringify({ featured })
    });
    console.log('Offer featured status updated:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error featuring offer:', error);
    throw error;
  }
}

// ============================================
// Usage Examples
// ============================================

// Example 1: Create an offer
// createOffer({
//   title: 'Instagram Post - Lifestyle',
//   description: 'High-quality lifestyle post on my Instagram account',
//   category: 'lifestyle',
//   priceUsd: 150.00,
//   priceCoins: 15000,
//   socialMediaType: 'instagram',
//   followersCount: 50000,
//   deliverables: [
//     { type: 'post', quantity: 1, description: 'Feed post with photo' },
//     { type: 'story', quantity: 3, description: 'Instagram stories' }
//   ],
//   requirements: [
//     { type: 'content', description: 'Brand must provide product', required: true }
//   ],
//   tags: ['lifestyle', 'fashion', 'instagram']
// });

// Example 2: Search offers
// searchOffers({
//   query: 'lifestyle',
//   category: 'fashion',
//   minPrice: 100,
//   maxPrice: 500,
//   platform: 'instagram',
//   sort: 'price_asc',
//   page: 1,
//   limit: 20
// });

// Example 3: AI search
// aiSearchOffers('I need a fitness influencer with 50k+ followers for a protein brand');

module.exports = {
  createOffer,
  listMyOffers,
  getOffer,
  updateOffer,
  deleteOffer,
  searchOffers,
  aiSearchOffers,
  getOfferBySlug,
  toggleOfferStatus,
  uploadOfferImages,
  adminListOffers,
  adminApproveOffer,
  adminRejectOffer,
  adminFeatureOffer
};
