#!/bin/bash

# =============================================================================
# Influqa API - Offers Management Examples (cURL)
# =============================================================================
# This file demonstrates offer operations using cURL commands
# 
# Usage:
#   chmod +x offers.sh
#   export INFLUQA_TOKEN="your_jwt_token"
#   ./offers.sh
# =============================================================================

API_BASE_URL="https://api.influqa.com/api/v1"
TOKEN="${INFLUQA_TOKEN:-your_jwt_token_here}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Influqa API - Offers Management${NC}"
echo "================================="
echo ""

# =============================================================================
# 1. Create Offer
# =============================================================================
echo -e "${GREEN}1. Create Offer${NC}"
echo "---------------"
echo "Create a new service offering"
echo ""

curl -X POST "${API_BASE_URL}/offers" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Instagram Post - Lifestyle",
    "description": "High-quality lifestyle post on my Instagram account with 50k+ engaged followers",
    "category": "lifestyle",
    "price_usd": 150.00,
    "price_coins": 15000,
    "social_media_type": "instagram",
    "followers_count": 50000,
    "deliverables": [
      {
        "type": "post",
        "quantity": 1,
        "description": "Feed post with professional photo"
      },
      {
        "type": "story",
        "quantity": 3,
        "description": "Instagram stories with swipe-up link"
      }
    ],
    "requirements": [
      {
        "type": "content",
        "description": "Brand must provide product or service for review",
        "required": true
      },
      {
        "type": "guidelines",
        "description": "Brand guidelines and key messaging points",
        "required": true
      }
    ],
    "tags": ["lifestyle", "fashion", "instagram", "photography"]
  }' | jq .

echo ""

# =============================================================================
# 2. List My Offers
# =============================================================================
echo -e "${GREEN}2. List My Offers${NC}"
echo "-----------------"
echo "Get all offers created by the authenticated user"
echo ""

curl -X GET "${API_BASE_URL}/influencer/offers?page=1&limit=20" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 3. List Offers with Filters
# =============================================================================
echo -e "${GREEN}3. List Offers with Filters${NC}"
echo "---------------------------"
echo "Filter offers by status and category"
echo ""

curl -X GET "${API_BASE_URL}/influencer/offers?status=active&category=lifestyle&page=1&limit=10" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 4. Get Offer Details
# =============================================================================
echo -e "${GREEN}4. Get Offer Details${NC}"
echo "--------------------"
echo "Get detailed information about a specific offer"
echo ""

OFFER_ID="offer_123456"

curl -X GET "${API_BASE_URL}/offers/${OFFER_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 5. Update Offer
# =============================================================================
echo -e "${GREEN}5. Update Offer${NC}"
echo "---------------"
echo "Update an existing offer"
echo ""

curl -X PUT "${API_BASE_URL}/offers/${OFFER_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Instagram Post - Lifestyle (Updated)",
    "price_usd": 175.00,
    "description": "Updated description with more details"
  }' | jq .

echo ""

# =============================================================================
# 6. Delete Offer
# =============================================================================
echo -e "${GREEN}6. Delete Offer${NC}"
echo "---------------"
echo "Delete an offer (soft delete)"
echo ""

curl -X DELETE "${API_BASE_URL}/offers/${OFFER_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 7. Toggle Offer Status
# =============================================================================
echo -e "${GREEN}7. Toggle Offer Status${NC}"
echo "----------------------"
echo "Activate or pause an offer"
echo ""

# Pause offer
echo "Pausing offer..."
curl -X PUT "${API_BASE_URL}/offers/${OFFER_ID}/status" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}' | jq .

echo ""

# Activate offer
echo "Activating offer..."
curl -X PUT "${API_BASE_URL}/offers/${OFFER_ID}/status" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"is_active": true}' | jq .

echo ""

# =============================================================================
# 8. Search Offers (Public)
# =============================================================================
echo -e "${BLUE}8. Search Offers (Public - No Auth Required)${NC}"
echo "--------------------------------------------"
echo "Search for offers with various filters"
echo ""

# Basic search
echo "Basic search..."
curl -X GET "${API_BASE_URL}/offers?q=lifestyle&page=1&limit=20" \
  -H "Content-Type: application/json" | jq .

echo ""

# Search with filters
echo "Search with filters..."
curl -X GET "${API_BASE_URL}/offers?category=fashion&min_price=100&max_price=500&platform=instagram&sort=price_asc&page=1&limit=20" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 9. Get Offer by Slug (Public)
# =============================================================================
echo -e "${BLUE}9. Get Offer by Slug (Public)${NC}"
echo "-----------------------------"
echo "Get offer details using URL-friendly slug"
echo ""

SLUG="instagram-post-lifestyle-abc123"

curl -X GET "${API_BASE_URL}/offers/slug/${SLUG}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 10. AI-Powered Search
# =============================================================================
echo -e "${GREEN}10. AI-Powered Search${NC}"
echo "---------------------"
echo "Search using natural language with AI"
echo ""

curl -X POST "${API_BASE_URL}/ai/search" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I need a fitness influencer with 50k+ followers for a protein brand campaign in the US"
  }' | jq .

echo ""

# =============================================================================
# 11. Admin: List All Offers
# =============================================================================
echo -e "${YELLOW}11. Admin: List All Offers${NC}"
echo "--------------------------"
echo "List all offers on the platform (Admin only)"
echo ""

curl -X GET "${API_BASE_URL}/admin/offers?status=pending_review&page=1&limit=50" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 12. Admin: Approve Offer
# =============================================================================
echo -e "${YELLOW}12. Admin: Approve Offer${NC}"
echo "------------------------"
echo "Approve a pending offer (Admin only)"
echo ""

curl -X POST "${API_BASE_URL}/admin/offers/${OFFER_ID}/approve" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 13. Admin: Reject Offer
# =============================================================================
echo -e "${YELLOW}13. Admin: Reject Offer${NC}"
echo "-----------------------"
echo "Reject a pending offer with reason (Admin only)"
echo ""

curl -X POST "${API_BASE_URL}/admin/offers/${OFFER_ID}/reject" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Offer does not meet our quality guidelines. Please review our content policy."
  }' | jq .

echo ""

# =============================================================================
# 14. Admin: Feature Offer
# =============================================================================
echo -e "${YELLOW}14. Admin: Feature Offer${NC}"
echo "------------------------"
echo "Mark an offer as featured (Admin only)"
echo ""

curl -X POST "${API_BASE_URL}/admin/offers/${OFFER_ID}/feature" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"featured": true}' | jq .

echo ""
