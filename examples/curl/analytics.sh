#!/bin/bash

# =============================================================================
# Influqa API - Analytics Examples (cURL)
# =============================================================================
# This file demonstrates analytics operations using cURL commands
# 
# Usage:
#   chmod +x analytics.sh
#   export INFLUQA_TOKEN="your_jwt_token"
#   ./analytics.sh
# =============================================================================

API_BASE_URL="https://api.influqa.com/api/v1"
TOKEN="${INFLUQA_TOKEN:-your_jwt_token_here}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Influqa API - Analytics${NC}"
echo "======================="
echo ""

# =============================================================================
# 1. Get Dashboard Analytics
# =============================================================================
echo -e "${GREEN}1. Get Dashboard Analytics${NC}"
echo "-------------------------"
echo "Get overview analytics for the dashboard"
echo ""

curl -X GET "${API_BASE_URL}/analytics/dashboard" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 2. Get Earnings Analytics
# =============================================================================
echo -e "${GREEN}2. Get Earnings Analytics${NC}"
echo "------------------------"
echo "Get earnings data with date range"
echo ""

# Using preset
curl -X GET "${API_BASE_URL}/analytics/earnings?preset=last_30_days" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# Using custom date range
echo "Custom date range..."
curl -X GET "${API_BASE_URL}/analytics/earnings?start_date=2026-01-01&end_date=2026-03-31" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 3. Get Performance Metrics
# =============================================================================
echo -e "${GREEN}3. Get Performance Metrics${NC}"
echo "-------------------------"
echo "Get detailed performance analytics"
echo ""

curl -X GET "${API_BASE_URL}/analytics/performance?preset=this_month" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 4. Export Analytics Data
# =============================================================================
echo -e "${GREEN}4. Export Analytics Data${NC}"
echo "-----------------------"
echo "Export analytics in various formats"
echo ""

# Export as CSV
echo "Export as CSV..."
curl -X GET "${API_BASE_URL}/analytics/export?format=csv&preset=last_30_days" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  --output "analytics_export.csv"

echo "CSV exported to analytics_export.csv"
echo ""

# Export as PDF
echo "Export as PDF..."
curl -X GET "${API_BASE_URL}/analytics/export?format=pdf&preset=this_month" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  --output "analytics_report.pdf"

echo "PDF exported to analytics_report.pdf"
echo ""

# Export as JSON
echo "Export as JSON..."
curl -X GET "${API_BASE_URL}/analytics/export?format=json&preset=last_7_days" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq . > analytics_data.json

echo "JSON exported to analytics_data.json"
echo ""

# =============================================================================
# 5. Track Custom Event
# =============================================================================
echo -e "${GREEN}5. Track Custom Event${NC}"
echo "--------------------"
echo "Send a custom analytics event"
echo ""

curl -X POST "${API_BASE_URL}/analytics/track" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "event": "offer_viewed",
    "properties": {
      "offer_id": "offer_123456",
      "category": "lifestyle",
      "source": "search_results"
    },
    "timestamp": "2026-03-23T10:30:00Z"
  }' | jq .

echo ""

# =============================================================================
# 6. Get Platform Stats (Admin)
# =============================================================================
echo -e "${YELLOW}6. Get Platform Stats (Admin)${NC}"
echo "-----------------------------"
echo "Get overall platform statistics (Admin only)"
echo ""

curl -X GET "${API_BASE_URL}/admin/stats" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# Available Date Presets
# =============================================================================
echo -e "${YELLOW}Available Date Presets:${NC}"
echo "----------------------"
echo "  - today"
echo "  - yesterday"
echo "  - last_7_days"
echo "  - last_30_days"
echo "  - this_month"
echo "  - last_month"
echo "  - this_year"
echo "  - last_year"
echo ""
