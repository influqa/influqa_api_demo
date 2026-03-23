/**
 * Influqa API - Orders Management Examples (JavaScript)
 * 
 * This file demonstrates order creation, management, and tracking operations
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
// 1. Create Order
// ============================================
async function createOrder(orderData) {
  try {
    const data = await apiRequest('/orders', {
      method: 'POST',
      body: JSON.stringify({
        offer_id: orderData.offerId,
        requirements: orderData.requirements,
        message: orderData.message,
        payment_method: orderData.paymentMethod, // 'stripe', 'coins'
        use_coins: orderData.useCoins || false,
        coins_amount: orderData.coinsAmount || 0
      })
    });
    console.log('Order created:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error creating order:', error);
    throw error;
  }
}

// ============================================
// 2. Get Order Details
// ============================================
async function getOrder(orderId) {
  try {
    const data = await apiRequest(`/orders/${orderId}`);
    console.log('Order details:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching order:', error);
    throw error;
  }
}

// ============================================
// 3. List My Orders (as Buyer)
// ============================================
async function listMyOrders(filters = {}) {
  try {
    const queryParams = new URLSearchParams();
    
    if (filters.status) queryParams.append('status', filters.status);
    if (filters.page) queryParams.append('page', filters.page.toString());
    if (filters.limit) queryParams.append('limit', filters.limit.toString());
    if (filters.sort) queryParams.append('sort', filters.sort);

    const data = await apiRequest(`/orders?${queryParams.toString()}`);
    console.log('My orders:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error listing orders:', error);
    throw error;
  }
}

// ============================================
// 4. List Orders as Seller
// ============================================
async function listSellerOrders(filters = {}) {
  try {
    const queryParams = new URLSearchParams();
    
    if (filters.status) queryParams.append('status', filters.status);
    if (filters.page) queryParams.append('page', filters.page.toString());
    if (filters.limit) queryParams.append('limit', filters.limit.toString());

    const data = await apiRequest(`/influencer/orders?${queryParams.toString()}`);
    console.log('Seller orders:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error listing seller orders:', error);
    throw error;
  }
}

// ============================================
// 5. Accept Order (Seller)
// ============================================
async function acceptOrder(orderId) {
  try {
    const data = await apiRequest(`/orders/${orderId}/accept`, {
      method: 'POST'
    });
    console.log('Order accepted:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error accepting order:', error);
    throw error;
  }
}

// ============================================
// 6. Reject Order (Seller)
// ============================================
async function rejectOrder(orderId, reason) {
  try {
    const data = await apiRequest(`/orders/${orderId}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    });
    console.log('Order rejected:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error rejecting order:', error);
    throw error;
  }
}

// ============================================
// 7. Start Order (Seller)
// ============================================
async function startOrder(orderId) {
  try {
    const data = await apiRequest(`/orders/${orderId}/start`, {
      method: 'POST'
    });
    console.log('Order started:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error starting order:', error);
    throw error;
  }
}

// ============================================
// 8. Deliver Order (Seller)
// ============================================
async function deliverOrder(orderId, deliveryData) {
  try {
    const data = await apiRequest(`/orders/${orderId}/deliver`, {
      method: 'POST',
      body: JSON.stringify({
        message: deliveryData.message,
        attachments: deliveryData.attachments || [],
        links: deliveryData.links || []
      })
    });
    console.log('Order delivered:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error delivering order:', error);
    throw error;
  }
}

// ============================================
// 9. Request Revision (Buyer)
// ============================================
async function requestRevision(orderId, revisionData) {
  try {
    const data = await apiRequest(`/orders/${orderId}/revision`, {
      method: 'POST',
      body: JSON.stringify({
        message: revisionData.message,
        requirements: revisionData.requirements
      })
    });
    console.log('Revision requested:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error requesting revision:', error);
    throw error;
  }
}

// ============================================
// 10. Complete Order (Buyer)
// ============================================
async function completeOrder(orderId) {
  try {
    const data = await apiRequest(`/orders/${orderId}/complete`, {
      method: 'POST'
    });
    console.log('Order completed:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error completing order:', error);
    throw error;
  }
}

// ============================================
// 11. Cancel Order
// ============================================
async function cancelOrder(orderId, reason) {
  try {
    const data = await apiRequest(`/orders/${orderId}/cancel`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    });
    console.log('Order cancelled:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error cancelling order:', error);
    throw error;
  }
}

// ============================================
// 12. Get Order Messages
// ============================================
async function getOrderMessages(orderId) {
  try {
    const data = await apiRequest(`/orders/${orderId}/messages`);
    console.log('Order messages:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error fetching order messages:', error);
    throw error;
  }
}

// ============================================
// 13. Send Order Message
// ============================================
async function sendOrderMessage(orderId, message, attachments = []) {
  try {
    const data = await apiRequest(`/orders/${orderId}/messages`, {
      method: 'POST',
      body: JSON.stringify({
        message: message,
        attachments: attachments
      })
    });
    console.log('Message sent:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error sending message:', error);
    throw error;
  }
}

// ============================================
// 14. Admin: List All Orders
// ============================================
async function adminListOrders(filters = {}) {
  try {
    const queryParams = new URLSearchParams();
    
    if (filters.status) queryParams.append('status', filters.status);
    if (filters.dateFrom) queryParams.append('date_from', filters.dateFrom);
    if (filters.dateTo) queryParams.append('date_to', filters.dateTo);
    if (filters.search) queryParams.append('search', filters.search);
    if (filters.page) queryParams.append('page', filters.page.toString());
    if (filters.limit) queryParams.append('limit', filters.limit.toString());

    const data = await apiRequest(`/admin/orders?${queryParams.toString()}`);
    console.log('Admin orders list:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error listing admin orders:', error);
    throw error;
  }
}

// ============================================
// 15. Admin: Cancel Order
// ============================================
async function adminCancelOrder(orderId, reason) {
  try {
    const data = await apiRequest(`/admin/orders/${orderId}/cancel`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    });
    console.log('Order cancelled by admin:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error cancelling order:', error);
    throw error;
  }
}

// ============================================
// 16. Admin: Refund Order
// ============================================
async function adminRefundOrder(orderId, refundData) {
  try {
    const data = await apiRequest(`/admin/orders/${orderId}/refund`, {
      method: 'POST',
      body: JSON.stringify({
        amount: refundData.amount,
        reason: refundData.reason,
        full_refund: refundData.fullRefund || false
      })
    });
    console.log('Order refunded:', data.data);
    return data.data;
  } catch (error) {
    console.error('Error refunding order:', error);
    throw error;
  }
}

// ============================================
// Usage Examples
// ============================================

// Example 1: Create an order
// createOrder({
//   offerId: 'offer_123456',
//   requirements: 'Please create a post featuring our new product',
//   message: 'Looking forward to working with you!',
//   paymentMethod: 'stripe',
//   useCoins: false
// });

// Example 2: Accept order (as seller)
// acceptOrder('order_789012');

// Example 3: Deliver order with attachments
// deliverOrder('order_789012', {
//   message: 'Here is the completed work!',
//   attachments: ['https://example.com/image1.jpg'],
//   links: ['https://instagram.com/p/ABC123']
// });

// Example 4: Complete order (as buyer)
// completeOrder('order_789012');

module.exports = {
  createOrder,
  getOrder,
  listMyOrders,
  listSellerOrders,
  acceptOrder,
  rejectOrder,
  startOrder,
  deliverOrder,
  requestRevision,
  completeOrder,
  cancelOrder,
  getOrderMessages,
  sendOrderMessage,
  adminListOrders,
  adminCancelOrder,
  adminRefundOrder
};
