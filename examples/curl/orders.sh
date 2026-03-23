#!/bin/bash

# =============================================================================
# Influqa API - Orders Management Examples (cURL)
# =============================================================================
# This file demonstrates order operations using cURL commands
# 
# Usage:
#   chmod +x orders.sh
#   export INFLUQA_TOKEN="your_jwt_token"
#   ./orders.sh
# =============================================================================

API_BASE_URL="https://api.influqa.com/api/v1"
TOKEN="${INFLUQA_TOKEN:-your_jwt_token_here}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Influqa API - Orders Management${NC}"
echo "================================="
echo ""

# =============================================================================
# 1. Create Order
# =============================================================================
echo -e "${GREEN}1. Create Order${NC}"
echo "---------------"
echo "Place an order for an offer"
echo ""

curl -X POST "${API_BASE_URL}/orders" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "offer_id": "offer_123456",
    "requirements": "Please create a post featuring our new protein powder. Include the product in action shots.",
    "message": "Looking forward to working with you! Let me know if you need any additional information.",
    "payment_method": "stripe",
    "use_coins": false
  }' | jq .

echo ""

# =============================================================================
# 2. Create Order with Coins
# =============================================================================
echo -e "${GREEN}2. Create Order with Coins${NC}"
echo "--------------------------"
echo "Place an order using Influqa Coins"
echo ""

curl -X POST "${API_BASE_URL}/orders" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "offer_id": "offer_123456",
    "requirements": "Create an Instagram story showcasing our app",
    "message": "Excited to collaborate!",
    "payment_method": "coins",
    "use_coins": true,
    "coins_amount": 15000
  }' | jq .

echo ""

# =============================================================================
# 3. Get Order Details
# =============================================================================
echo -e "${GREEN}3. Get Order Details${NC}"
echo "--------------------"
echo "Get detailed information about a specific order"
echo ""

ORDER_ID="order_789012"

curl -X GET "${API_BASE_URL}/orders/${ORDER_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 4. List My Orders (as Buyer)
# =============================================================================
echo -e "${GREEN}4. List My Orders (Buyer)${NC}"
echo "-------------------------"
echo "Get all orders placed by the authenticated user"
echo ""

curl -X GET "${API_BASE_URL}/orders?page=1&limit=20&sort=created_at&order=desc" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 5. List Orders with Status Filter
# =============================================================================
echo -e "${GREEN}5. List Orders with Status Filter${NC}"
echo "---------------------------------"
echo "Filter orders by status"
echo ""

# Pending orders
echo "Pending orders..."
curl -X GET "${API_BASE_URL}/orders?status=pending&page=1&limit=10" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# In progress orders
echo "In progress orders..."
curl -X GET "${API_BASE_URL}/orders?status=in_progress&page=1&limit=10" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 6. List Orders as Seller
# =============================================================================
echo -e "${GREEN}6. List Orders as Seller${NC}"
echo "------------------------"
echo "Get all orders received by the authenticated seller"
echo ""

curl -X GET "${API_BASE_URL}/influencer/orders?page=1&limit=20" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 7. Accept Order (Seller)
# =============================================================================
echo -e "${GREEN}7. Accept Order (Seller)${NC}"
echo "------------------------"
echo "Accept a pending order as seller"
echo ""

curl -X POST "${API_BASE_URL}/orders/${ORDER_ID}/accept" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 8. Reject Order (Seller)
# =============================================================================
echo -e "${GREEN}8. Reject Order (Seller)${NC}"
echo "------------------------"
echo "Reject a pending order with reason"
echo ""

curl -X POST "${API_BASE_URL}/orders/${ORDER_ID}/reject" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Unfortunately, I am not available during your requested timeframe. Please try again in 2 weeks."
  }' | jq .

echo ""

# =============================================================================
# 9. Start Order (Seller)
# =============================================================================
echo -e "${GREEN}9. Start Order (Seller)${NC}"
echo "-----------------------"
echo "Mark order as in progress"
echo ""

curl -X POST "${API_BASE_URL}/orders/${ORDER_ID}/start" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 10. Deliver Order (Seller)
# =============================================================================
echo -e "${GREEN}10. Deliver Order (Seller)${NC}"
echo "--------------------------"
echo "Submit completed work for the order"
echo ""

curl -X POST "${API_BASE_URL}/orders/${ORDER_ID}/deliver" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Here is the completed work! I have created the Instagram post and stories as requested. The content is live and performing well with high engagement.",
    "attachments": [
      "https://example.com/delivery/image1.jpg",
      "https://example.com/delivery/image2.jpg"
    ],
    "links": [
      "https://instagram.com/p/ABC123xyz",
      "https://instagram.com/stories/highlights/XYZ789"
    ]
  }' | jq .

echo ""

# =============================================================================
# 11. Request Revision (Buyer)
# =============================================================================
echo -e "${GREEN}11. Request Revision (Buyer)${NC}"
echo "----------------------------"
echo "Request changes to delivered work"
echo ""

curl -X POST "${API_BASE_URL}/orders/${ORDER_ID}/revision" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "The post looks great! Could you please add the hashtag #ProteinLife to the caption? Also, could you tag our official account @brandname?",
    "requirements": "Add hashtag and tag brand account"
  }' | jq .

echo ""

# =============================================================================
# 12. Complete Order (Buyer)
# =============================================================================
echo -e "${GREEN}12. Complete Order (Buyer)${NC}"
echo "--------------------------"
echo "Mark order as complete and release payment"
echo ""

curl -X POST "${API_BASE_URL}/orders/${ORDER_ID}/complete" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 13. Cancel Order
# =============================================================================
echo -e "${GREEN}13. Cancel Order${NC}"
echo "----------------"
echo "Cancel an order with reason"
echo ""

curl -X POST "${API_BASE_URL}/orders/${ORDER_ID}/cancel" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Project requirements have changed. We no longer need this service."
  }' | jq .

echo ""

# =============================================================================
# 14. Get Order Messages
# =============================================================================
echo -e "${GREEN}14. Get Order Messages${NC}"
echo "----------------------"
echo "Get all messages in an order"
echo ""

curl -X GET "${API_BASE_URL}/orders/${ORDER_ID}/messages" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 15. Send Order Message
# =============================================================================
echo -e "${GREEN}15. Send Order Message${NC}"
echo "----------------------"
echo "Send a message in the order chat"
echo ""

curl -X POST "${API_BASE_URL}/orders/${ORDER_ID}/messages" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hi! I have a question about the requirements. Could you clarify the brand colors you prefer?",
    "attachments": []
  }' | jq .

echo ""

# =============================================================================
# 16. Admin: List All Orders
# =============================================================================
echo -e "${YELLOW}16. Admin: List All Orders${NC}"
echo "--------------------------"
echo "List all orders on the platform (Admin only)"
echo ""

curl -X GET "${API_BASE_URL}/admin/orders?page=1&limit=50" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 17. Admin: Cancel Order
# =============================================================================
echo -e "${YELLOW}17. Admin: Cancel Order${NC}"
echo "-----------------------"
echo "Cancel any order as admin (Admin only)"
echo ""

curl -X POST "${API_BASE_URL}/admin/orders/${ORDER_ID}/cancel" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Order cancelled due to violation of platform terms"
  }' | jq .

echo ""

# =============================================================================
# 18. Admin: Refund Order
# =============================================================================
echo -e "${YELLOW}18. Admin: Refund Order${NC}"
echo "-----------------------"
echo "Process refund for an order (Admin only)"
echo ""

# Full refund
echo "Full refund..."
curl -X POST "${API_BASE_URL}/admin/orders/${ORDER_ID}/refund" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "full_refund": true,
    "reason": "Service not delivered as described"
  }' | jq .

echo ""

# Partial refund
echo "Partial refund..."
curl -X POST "${API_BASE_URL}/admin/orders/${ORDER_ID}/refund" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 75.00,
    "full_refund": false,
    "reason": "Partial delivery - only 50% of requirements met"
  }' | jq .

echo ""
