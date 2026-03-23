#!/bin/bash

# =============================================================================
# Influqa API - Authentication Examples (cURL)
# =============================================================================
# This file demonstrates authentication operations using cURL commands
# 
# Usage:
#   chmod +x auth.sh
#   ./auth.sh
#
# Or run individual commands directly in your terminal
# =============================================================================

API_BASE_URL="https://api.influqa.com/api/v1"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Influqa API - Authentication Examples${NC}"
echo "======================================"
echo ""

# =============================================================================
# 1. User Login
# =============================================================================
echo -e "${GREEN}1. User Login${NC}"
echo "-------------"
echo "Authenticate user and get JWT token"
echo ""

curl -X POST "${API_BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "your_password"
  }' | jq .

echo ""
echo "Response will contain:"
echo "  - token: JWT token for authentication"
echo "  - user: User profile information"
echo ""

# =============================================================================
# 2. User Registration
# =============================================================================
echo -e "${GREEN}2. User Registration${NC}"
echo "--------------------"
echo "Create a new user account"
echo ""

curl -X POST "${API_BASE_URL}/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "secure_password",
    "full_name": "John Doe",
    "user_type": "influencer",
    "username": "johndoe"
  }' | jq .

echo ""
echo "User types: influencer, brand, agency"
echo ""

# =============================================================================
# 3. Refresh Token
# =============================================================================
echo -e "${GREEN}3. Refresh Token${NC}"
echo "----------------"
echo "Get a new JWT token before the current one expires"
echo ""

# Replace with your actual token
TOKEN="your_jwt_token_here"

curl -X POST "${API_BASE_URL}/auth/refresh" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 4. Logout
# =============================================================================
echo -e "${GREEN}4. Logout${NC}"
echo "---------"
echo "Invalidate the current JWT token"
echo ""

curl -X POST "${API_BASE_URL}/auth/logout" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# 5. Google OAuth Login
# =============================================================================
echo -e "${GREEN}5. Google OAuth Login${NC}"
echo "---------------------"
echo "Initiate Google OAuth flow"
echo ""

echo "Open this URL in your browser:"
echo "${API_BASE_URL}/auth/google"
echo ""
echo "After authentication, you'll be redirected to the callback URL"
echo "with a code parameter. Use that code to complete authentication."
echo ""

# =============================================================================
# 6. Google OAuth Callback
# =============================================================================
echo -e "${GREEN}6. Google OAuth Callback${NC}"
echo "------------------------"
echo "Complete Google OAuth with the authorization code"
echo ""

# Replace with the code from the callback
AUTH_CODE="authorization_code_from_callback"

curl -X GET "${API_BASE_URL}/auth/google/callback?code=${AUTH_CODE}" \
  -H "Content-Type: application/json" | jq .

echo ""

# =============================================================================
# Example: Store token in variable for subsequent requests
# =============================================================================
echo -e "${YELLOW}Tip: Store your token in an environment variable${NC}"
echo ""
echo "export INFLUQA_TOKEN='your_jwt_token_here'"
echo ""
echo "Then use it in requests:"
echo 'curl -H "Authorization: Bearer $INFLUQA_TOKEN" ...'
echo ""
