/**
 * Influqa API - Analytics Examples (JavaScript)
 * 
 * This file demonstrates analytics and reporting operations
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
// 1. Get Dashboard Analytics
// ============================================
async function getDashboardAnalytics() {
  try {
    const data = await apiRequest('/analytics/dashboard');
    console.log('Dashboard analytics:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching dashboard:', error);
    throw error;
  }
}

// ============================================
// 2. Get Earnings Analytics
// ============================================
async function getEarningsAnalytics(dateRange) {
  try {
    const queryParams = new URLSearchParams();
    
    if (dateRange.preset) {
      queryParams.append('preset', dateRange.preset);
    } else if (dateRange.custom) {
      queryParams.append('start_date', dateRange.custom.start);
      queryParams.append('end_date', dateRange.custom.end);
    }

    const data = await apiRequest(`/analytics/earnings?${queryParams.toString()}`);
    console.log('Earnings analytics:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching earnings:', error);
    throw error;
  }
}

// ============================================
// 3. Get Performance Metrics
// ============================================
async function getPerformanceMetrics(dateRange) {
  try {
    const queryParams = new URLSearchParams();
    
    if (dateRange.preset) {
      queryParams.append('preset', dateRange.preset);
    }

    const data = await apiRequest(`/analytics/performance?${queryParams.toString()}`);
    console.log('Performance metrics:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching performance:', error);
    throw error;
  }
}

// ============================================
// 4. Export Analytics Data
// ============================================
async function exportAnalytics(format, dateRange) {
  try {
    const queryParams = new URLSearchParams();
    queryParams.append('format', format); // 'pdf', 'csv', 'xlsx', 'json'
    
    if (dateRange.preset) {
      queryParams.append('preset', dateRange.preset);
    } else if (dateRange.custom) {
      queryParams.append('start_date', dateRange.custom.start);
      queryParams.append('end_date', dateRange.custom.end);
    }

    const token = getAuthToken();
    const response = await fetch(`${API_BASE_URL}/analytics/export?${queryParams.toString()}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    // Handle file download
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `analytics_export.${format}`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    console.log(`Analytics exported as ${format}`);
  } catch (error) {
    console.error('Error exporting analytics:', error);
    throw error;
  }
}

// ============================================
// 5. Track Custom Event
// ============================================
async function trackEvent(eventName, properties) {
  try {
    const data = await apiRequest('/analytics/track', {
      method: 'POST',
      body: JSON.stringify({
        event: eventName,
        properties: properties,
        timestamp: new Date().toISOString()
      })
    });
    console.log('Event tracked:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error tracking event:', error);
    throw error;
  }
}

// ============================================
// 6. Get Platform Stats (Admin)
// ============================================
async function getPlatformStats() {
  try {
    const data = await apiRequest('/admin/stats');
    console.log('Platform stats:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching platform stats:', error);
    throw error;
  }
}

// ============================================
// Usage Examples
// ============================================

// Example 1: Get dashboard
// getDashboardAnalytics();

// Example 2: Get earnings with preset
// getEarningsAnalytics({ preset: 'last_30_days' });

// Example 3: Get earnings with custom range
// getEarningsAnalytics({
//   custom: {
//     start: '2026-01-01',
//     end: '2026-03-31'
//   }
// });

// Example 4: Export analytics
// exportAnalytics('pdf', { preset: 'this_month' });

// Example 5: Track custom event
// trackEvent('offer_viewed', {
//   offer_id: 'offer_123456',
//   category: 'lifestyle',
//   source: 'search_results'
// });

// Available presets: 'today', 'yesterday', 'last_7_days', 'last_30_days', 
// 'this_month', 'last_month', 'this_year', 'last_year'

module.exports = {
  getDashboardAnalytics,
  getEarningsAnalytics,
  getPerformanceMetrics,
  exportAnalytics,
  trackEvent,
  getPlatformStats
};
