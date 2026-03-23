/**
 * Influqa API - Coins System Examples (JavaScript)
 * 
 * This file demonstrates the Influqa Coins virtual currency system operations
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
// 1. Get Coin Balance
// ============================================
async function getCoinBalance() {
  try {
    const data = await apiRequest('/coins/balance');
    console.log('Coin balance:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching coin balance:', error);
    throw error;
  }
}

// ============================================
// 2. Purchase Coins
// ============================================
async function purchaseCoins(packageId, paymentMethod = 'stripe') {
  try {
    const data = await apiRequest('/coins/purchase', {
      method: 'POST',
      body: JSON.stringify({
        package_id: packageId,
        payment_method: paymentMethod
      })
    });
    console.log('Purchase initiated:', data.data);
    
    // If Stripe payment is required, redirect to checkout
    if (data.data.checkout_url) {
      window.location.href = data.data.checkout_url;
    }
    
    return data.data;
  } catch (error) {
    console.error('Error purchasing coins:', error);
    throw error;
  }
}

// ============================================
// 3. Get Available Coin Packages
// ============================================
async function getCoinPackages() {
  try {
    const data = await apiRequest('/coins/packages');
    console.log('Coin packages:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching coin packages:', error);
    throw error;
  }
}

// ============================================
// 4. Spend Coins
// ============================================
async function spendCoins(amount, purpose, referenceId = null) {
  try {
    const data = await apiRequest('/coins/spend', {
      method: 'POST',
      body: JSON.stringify({
        amount: amount,
        purpose: purpose,
        reference_id: referenceId
      })
    });
    console.log('Coins spent:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error spending coins:', error);
    throw error;
  }
}

// ============================================
// 5. Convert Coins to USD
// ============================================
async function convertCoinsToUsd(coinsAmount) {
  try {
    const data = await apiRequest('/coins/convert', {
      method: 'POST',
      body: JSON.stringify({
        coins: coinsAmount,
        direction: 'to_usd'
      })
    });
    console.log('Conversion result:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error converting coins:', error);
    throw error;
  }
}

// ============================================
// 6. Get Transaction History
// ============================================
async function getTransactionHistory(filters = {}) {
  try {
    const queryParams = new URLSearchParams();
    
    if (filters.type) queryParams.append('type', filters.type); // 'purchase', 'spend', 'earn', 'gift'
    if (filters.startDate) queryParams.append('start_date', filters.startDate);
    if (filters.endDate) queryParams.append('end_date', filters.endDate);
    if (filters.page) queryParams.append('page', filters.page.toString());
    if (filters.limit) queryParams.append('limit', filters.limit.toString());

    const data = await apiRequest(`/coins/transactions?${queryParams.toString()}`);
    console.log('Transaction history:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching transaction history:', error);
    throw error;
  }
}

// ============================================
// 7. Send Gift (Coins to another user)
// ============================================
async function sendGift(recipientId, amount, message = '') {
  try {
    const data = await apiRequest('/coins/gift', {
      method: 'POST',
      body: JSON.stringify({
        recipient_id: recipientId,
        amount: amount,
        message: message
      })
    });
    console.log('Gift sent:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error sending gift:', error);
    throw error;
  }
}

// ============================================
// 8. Get Coin Exchange Rate
// ============================================
async function getCoinExchangeRate() {
  try {
    const data = await apiRequest('/coins/exchange-rate');
    console.log('Exchange rate:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching exchange rate:', error);
    throw error;
  }
}

// ============================================
// 9. Earn Coins (Complete tasks)
// ============================================
async function earnCoins(taskType) {
  try {
    const data = await apiRequest('/coins/earn', {
      method: 'POST',
      body: JSON.stringify({
        task_type: taskType // 'daily_login', 'complete_profile', 'refer_friend', etc.
      })
    });
    console.log('Coins earned:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error earning coins:', error);
    throw error;
  }
}

// ============================================
// 10. Get Available Tasks
// ============================================
async function getAvailableTasks() {
  try {
    const data = await apiRequest('/coins/tasks');
    console.log('Available tasks:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
}

// ============================================
// 11. Admin: Adjust User Balance
// ============================================
async function adminAdjustBalance(userId, amount, reason) {
  try {
    const data = await apiRequest('/admin/coins/adjust', {
      method: 'POST',
      body: JSON.stringify({
        user_id: userId,
        amount: amount, // Can be positive or negative
        reason: reason
      })
    });
    console.log('Balance adjusted:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error adjusting balance:', error);
    throw error;
  }
}

// ============================================
// 12. Admin: Get Platform Coin Stats
// ============================================
async function adminGetCoinStats() {
  try {
    const data = await apiRequest('/admin/coins/stats');
    console.log('Coin stats:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching coin stats:', error);
    throw error;
  }
}

// ============================================
// Usage Examples
// ============================================

// Example 1: Check balance
// getCoinBalance().then(balance => console.log(`You have ${balance.amount} coins`));

// Example 2: Purchase coins
// purchaseCoins('pkg_premium_1000', 'stripe');

// Example 3: Send gift
// sendGift('user_123456', 100, 'Thanks for the great work!');

// Example 4: Get transaction history
// getTransactionHistory({
//   type: 'purchase',
//   page: 1,
//   limit: 10
// });

// Example 5: Earn coins by completing task
// earnCoins('complete_profile');

module.exports = {
  getCoinBalance,
  purchaseCoins,
  getCoinPackages,
  spendCoins,
  convertCoinsToUsd,
  getTransactionHistory,
  sendGift,
  getCoinExchangeRate,
  earnCoins,
  getAvailableTasks,
  adminAdjustBalance,
  adminGetCoinStats
};
