# Influqa API Reference

Complete reference documentation for the Influqa API.

## Table of Contents

- [Authentication](#authentication)
- [Users](#users)
- [Offers](#offers)
- [Orders](#orders)
- [Analytics](#analytics)
- [Coins](#coins)
- [Currency](#currency)
- [Disputes](#disputes)
- [Support Tickets](#support-tickets)
- [AI Services](#ai-services)
- [Admin](#admin)
- [Payments](#payments)

---

## Authentication

### POST /auth/login

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "id": "usr_123456",
      "email": "user@example.com",
      "full_name": "John Doe",
      "user_type": "influencer"
    }
  }
}
```

### POST /auth/register

Create a new user account.

**Request Body:**
```json
{
  "email": "newuser@example.com",
  "password": "securePassword123",
  "full_name": "John Doe",
  "user_type": "influencer",
  "username": "johndoe"
}
```

**User Types:** `influencer`, `brand`, `agency`, `business`, `nonprofit`, `education`

---

## Users

### GET /users/me

Get current user profile.

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "usr_123456",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "user_type": "influencer",
    "vip_tier": "gold",
    "coins_balance": 5000,
    "profile": {
      "bio": "Content creator...",
      "avatar_url": "https://...",
      "country": "US",
      "city": "New York"
    }
  }
}
```

### PUT /users/me

Update user profile.

**Request Body:**
```json
{
  "full_name": "John Updated",
  "bio": "Updated bio",
  "country": "US",
  "city": "Los Angeles"
}
```

---

## Offers

### GET /offers

Search offers (public endpoint).

**Query Parameters:**
- `q` - Search query
- `category` - Filter by category
- `min_price` - Minimum price
- `max_price` - Maximum price
- `platform` - Social media platform
- `country` - Creator country
- `sort` - Sort order (price_asc, price_desc, newest, popular)
- `page` - Page number
- `limit` - Items per page (max 100)

### POST /offers

Create a new offer (requires authentication).

**Request Body:**
```json
{
  "title": "Instagram Post",
  "description": "High-quality post...",
  "category": "lifestyle",
  "price_usd": 150.00,
  "price_coins": 15000,
  "social_media_type": "instagram",
  "followers_count": 50000,
  "deliverables": [
    {
      "type": "post",
      "quantity": 1,
      "description": "Feed post"
    }
  ],
  "tags": ["lifestyle", "fashion"]
}
```

### GET /offers/:id

Get offer details.

### PUT /offers/:id

Update offer.

### DELETE /offers/:id

Delete offer (soft delete).

---

## Orders

### POST /orders

Create a new order.

**Request Body:**
```json
{
  "offer_id": "offer_123456",
  "requirements": "Please create...",
  "message": "Looking forward...",
  "payment_method": "stripe",
  "use_coins": false
}
```

### GET /orders

List my orders (as buyer).

### GET /orders/:id

Get order details.

### POST /orders/:id/accept

Accept order (seller).

### POST /orders/:id/reject

Reject order (seller).

**Request Body:**
```json
{
  "reason": "Not available..."
}
```

### POST /orders/:id/start

Start order (seller).

### POST /orders/:id/deliver

Deliver order (seller).

**Request Body:**
```json
{
  "message": "Here is the work...",
  "attachments": ["https://..."],
  "links": ["https://..."]
}
```

### POST /orders/:id/complete

Complete order (buyer).

### POST /orders/:id/cancel

Cancel order.

**Request Body:**
```json
{
  "reason": "Changed requirements..."
}
```

---

## Analytics

### GET /analytics/dashboard

Get dashboard analytics.

### GET /analytics/earnings

Get earnings data.

**Query Parameters:**
- `preset` - Date preset (today, yesterday, last_7_days, last_30_days, this_month, last_month, this_year, last_year)
- `start_date` - Custom start date (YYYY-MM-DD)
- `end_date` - Custom end date (YYYY-MM-DD)

### GET /analytics/performance

Get performance metrics.

### GET /analytics/export

Export analytics data.

**Query Parameters:**
- `format` - Export format (pdf, csv, xlsx, json)
- `preset` - Date preset

### POST /analytics/track

Track custom event.

**Request Body:**
```json
{
  "event": "offer_viewed",
  "properties": {
    "offer_id": "offer_123456",
    "category": "lifestyle"
  }
}
```

---

## Coins

### GET /coins/balance

Get current coin balance.

### GET /coins/packages

Get available coin packages.

### POST /coins/purchase

Purchase coins.

**Request Body:**
```json
{
  "package_id": "pkg_premium_1000",
  "payment_method": "stripe"
}
```

### POST /coins/spend

Spend coins.

**Request Body:**
```json
{
  "amount": 1000,
  "purpose": "order_payment",
  "reference_id": "order_123456"
}
```

### GET /coins/transactions

Get transaction history.

**Query Parameters:**
- `type` - Transaction type (purchase, spend, earn, gift)
- `start_date` - Start date
- `end_date` - End date
- `page` - Page number
- `limit` - Items per page

### POST /coins/gift

Send coins as gift.

**Request Body:**
```json
{
  "recipient_id": "usr_789012",
  "amount": 500,
  "message": "Thanks for the great work!"
}
```

---

## Currency

### GET /currency/rates

Get current exchange rates (public).

### POST /currency/convert

Convert currency (public).

**Request Body:**
```json
{
  "amount": 100,
  "from": "USD",
  "to": "EUR"
}
```

---

## Disputes

### GET /disputes

List disputes.

### POST /disputes

Create dispute.

**Request Body:**
```json
{
  "order_id": "order_123456",
  "reason": "service_not_delivered",
  "description": "The seller did not deliver...",
  "evidence": ["https://..."]
}
```

### GET /disputes/:id

Get dispute details.

### POST /disputes/:id/messages

Add message to dispute.

---

## Support Tickets

### GET /support/tickets

List support tickets.

### POST /support/tickets

Create support ticket.

**Request Body:**
```json
{
  "subject": "Payment issue",
  "category": "billing",
  "message": "I was charged twice...",
  "priority": "high"
}
```

### GET /support/tickets/:id

Get ticket details.

### POST /support/tickets/:id/messages

Send message in ticket.

### POST /support/tickets/:id/close

Close ticket.

---

## AI Services

### POST /ai/chat

AI chat assistant.

**Request Body:**
```json
{
  "message": "How do I create an offer?",
  "context": "onboarding"
}
```

### POST /ai/search

AI-powered search.

**Request Body:**
```json
{
  "query": "I need a fitness influencer with 50k followers..."
}
```

### POST /ai/generate

Generate content.

**Request Body:**
```json
{
  "type": "offer_description",
  "title": "Instagram Post",
  "category": "lifestyle",
  "features": ["high quality", "engaged audience"]
}
```

---

## Admin

All admin endpoints require admin privileges.

### GET /admin/users

List all users.

### GET /admin/offers

List all offers.

### GET /admin/orders

List all orders.

### GET /admin/stats

Get platform statistics.

---

## Payments

### GET /payments/stripe/setup

Setup Stripe account.

### POST /payments/stripe/connect

Connect Stripe account.

### GET /payments/stripe/account

Get Stripe account status.

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_TOKEN | 401 | JWT token is invalid or expired |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| INSUFFICIENT_FUNDS | 400 | Not enough balance/coins |
| RESOURCE_NOT_FOUND | 404 | Resource doesn't exist |
| VALIDATION_ERROR | 400 | Invalid request parameters |
| PERMISSION_DENIED | 403 | Insufficient permissions |
| STRIPE_ERROR | 400 | Payment processing error |

---

For more information, visit [docs.influqa.com](https://docs.influqa.com)
