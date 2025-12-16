# LegalMitra Monetization Implementation Plan
## Technical Implementation Details

---

## **Phase 1: User Authentication & Subscription Foundation**

### **1.1 Database Schema**

**Tables Needed:**

```sql
-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    email_verified BOOLEAN DEFAULT FALSE,
    subscription_tier VARCHAR(20) DEFAULT 'free', -- free, premium, professional
    subscription_status VARCHAR(20) DEFAULT 'active', -- active, cancelled, expired
    subscription_expires_at TIMESTAMP
);

-- Subscriptions Table
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    tier VARCHAR(20) NOT NULL, -- free, premium, professional
    status VARCHAR(20) NOT NULL, -- active, cancelled, expired
    started_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP,
    payment_method VARCHAR(50), -- razorpay, stripe, etc.
    payment_id VARCHAR(255),
    amount DECIMAL(10,2),
    billing_cycle VARCHAR(20), -- monthly, annual
    auto_renew BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usage Tracking Table
CREATE TABLE usage_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    feature_type VARCHAR(50) NOT NULL, -- query, document_draft, document_review, api_call
    resource_id VARCHAR(255), -- query_id, document_id, etc.
    metadata JSONB, -- additional data
    created_at TIMESTAMP DEFAULT NOW()
);

-- Daily Usage Summary (for rate limiting)
CREATE TABLE daily_usage (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    date DATE NOT NULL,
    query_count INT DEFAULT 0,
    document_draft_count INT DEFAULT 0,
    document_review_count INT DEFAULT 0,
    api_call_count INT DEFAULT 0,
    UNIQUE(user_id, date)
);

-- Conversations/Query History
CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    query_text TEXT NOT NULL,
    query_type VARCHAR(50), -- research, drafting, case_search, etc.
    response_text TEXT,
    metadata JSONB, -- AI model used, tokens, etc.
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Documents (for Premium/Professional)
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    team_id UUID, -- NULL for individual, set for team documents
    document_type VARCHAR(50), -- draft, review, template
    title VARCHAR(255),
    content TEXT,
    file_path VARCHAR(500), -- if uploaded file
    file_type VARCHAR(50),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Teams (for Professional tier)
CREATE TABLE teams (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_id UUID REFERENCES users(id),
    subscription_tier VARCHAR(20) DEFAULT 'professional',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Team Members
CREATE TABLE team_members (
    id UUID PRIMARY KEY,
    team_id UUID REFERENCES teams(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(50) DEFAULT 'member', -- owner, admin, member
    joined_at TIMESTAMP DEFAULT NOW()
);
```

### **1.2 Backend API Endpoints Needed**

```python
# Authentication
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
POST   /api/v1/auth/forgot-password
POST   /api/v1/auth/reset-password

# User Management
GET    /api/v1/user/profile
PUT    /api/v1/user/profile
GET    /api/v1/user/usage
GET    /api/v1/user/subscription

# Subscriptions
GET    /api/v1/subscriptions/plans
POST   /api/v1/subscriptions/create
POST   /api/v1/subscriptions/cancel
POST   /api/v1/subscriptions/upgrade
POST   /api/v1/subscriptions/downgrade
GET    /api/v1/subscriptions/invoices

# Conversations
GET    /api/v1/conversations
GET    /api/v1/conversations/{id}
POST   /api/v1/conversations
DELETE /api/v1/conversations/{id}
GET    /api/v1/conversations/search

# Documents
GET    /api/v1/documents
GET    /api/v1/documents/{id}
POST   /api/v1/documents
PUT    /api/v1/documents/{id}
DELETE /api/v1/documents/{id}
POST   /api/v1/documents/export

# Teams (Professional)
GET    /api/v1/teams
POST   /api/v1/teams
GET    /api/v1/teams/{id}
POST   /api/v1/teams/{id}/members
DELETE /api/v1/teams/{id}/members/{user_id}

# API Keys (Professional)
GET    /api/v1/api-keys
POST   /api/v1/api-keys
DELETE /api/v1/api-keys/{id}
```

### **1.3 Middleware for Usage Tracking**

```python
# backend/app/middleware/usage_tracking.py
from fastapi import Request, HTTPException
from app.models.user import User
from app.models.usage import UsageLog, DailyUsage

async def track_usage(request: Request, feature_type: str, resource_id: str = None):
    """Track user usage for rate limiting and analytics"""
    user = request.state.user  # Set by auth middleware
    
    # Check daily limits based on tier
    if not await check_usage_limit(user, feature_type):
        raise HTTPException(
            status_code=429,
            detail=f"Usage limit exceeded. Upgrade to Premium/Professional for unlimited access."
        )
    
    # Log usage
    await UsageLog.create(
        user_id=user.id,
        feature_type=feature_type,
        resource_id=resource_id
    )
    
    # Update daily counter
    await DailyUsage.increment(user.id, feature_type)
```

---

## **Phase 2: Feature Gating Implementation**

### **2.1 Feature Access Control**

```python
# backend/app/services/feature_access.py

TIER_FEATURES = {
    'free': {
        'queries_per_day': 5,
        'document_drafting': False,
        'document_review': False,
        'conversation_history': False,
        'export_responses': False,
        'api_access': False,
        'team_features': False,
        'response_length': 4000,  # tokens
        'ai_model': 'basic'
    },
    'premium': {
        'queries_per_day': -1,  # unlimited
        'document_drafting': True,
        'document_draft_limit': 10,  # per month
        'document_review': True,
        'document_review_limit': 50,  # per month
        'conversation_history': True,
        'history_retention_days': 30,
        'export_responses': True,
        'api_access': False,
        'team_features': False,
        'response_length': 8000,
        'ai_model': 'enhanced'
    },
    'professional': {
        'queries_per_day': -1,
        'document_drafting': True,
        'document_draft_limit': -1,  # unlimited
        'document_review': True,
        'document_review_limit': -1,
        'conversation_history': True,
        'history_retention_days': 365,
        'export_responses': True,
        'api_access': True,
        'api_rate_limit': 1000,  # per day
        'team_features': True,
        'response_length': 16000,
        'ai_model': 'best'
    }
}

async def check_feature_access(user: User, feature: str) -> bool:
    """Check if user's tier allows access to a feature"""
    tier = user.subscription_tier
    features = TIER_FEATURES.get(tier, TIER_FEATURES['free'])
    return features.get(feature, False)

async def check_usage_limit(user: User, feature: str) -> bool:
    """Check if user has reached usage limit for a feature"""
    tier = user.subscription_tier
    features = TIER_FEATURES.get(tier, TIER_FEATURES['free'])
    limit = features.get(f'{feature}_limit', None)
    
    if limit is None or limit == -1:
        return True  # No limit or unlimited
    
    # Check monthly usage
    usage_count = await get_monthly_usage(user.id, feature)
    return usage_count < limit
```

### **2.2 API Rate Limiting**

```python
# backend/app/middleware/rate_limiter.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Apply to endpoints
@router.post("/research")
@limiter.limit("5/day")  # For free tier, override for premium/professional
async def research(request: Request, ...):
    user = request.state.user
    tier = user.subscription_tier
    
    if tier == 'free':
        # Check daily limit
        if not await check_daily_limit(user, 'queries'):
            raise HTTPException(429, "Daily limit reached. Upgrade to Premium.")
    # Premium/Professional: unlimited
```

---

## **Phase 3: Payment Integration**

### **3.1 Payment Gateway Setup**

**Razorpay Integration (Recommended for India):**

```python
# backend/app/services/payment.py
import razorpay
from app.core.config import settings

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

async def create_subscription(user_id: str, plan_id: str, billing_cycle: str):
    """Create a subscription payment"""
    amount = get_plan_amount(plan_id, billing_cycle)
    
    order = razorpay_client.order.create({
        'amount': amount * 100,  # Convert to paise
        'currency': 'INR',
        'receipt': f'sub_{user_id}_{plan_id}',
        'notes': {
            'user_id': user_id,
            'plan_id': plan_id,
            'billing_cycle': billing_cycle
        }
    })
    
    return order

async def verify_payment(payment_id: str, order_id: str):
    """Verify payment and activate subscription"""
    payment = razorpay_client.payment.fetch(payment_id)
    
    if payment['status'] == 'captured':
        # Activate subscription
        await activate_subscription(user_id, plan_id)
        return True
    return False
```

### **3.2 Subscription Management**

```python
# backend/app/services/subscription.py

async def upgrade_subscription(user_id: str, new_tier: str):
    """Upgrade user subscription"""
    user = await User.get(user_id)
    current_tier = user.subscription_tier
    
    # Check if upgrade is valid
    if not is_valid_upgrade(current_tier, new_tier):
        raise ValueError("Invalid upgrade path")
    
    # Calculate prorated amount
    # Process payment
    # Update subscription
    # Send confirmation email
```

---

## **Phase 4: Frontend Enhancements**

### **4.1 Subscription Management UI**

```html
<!-- frontend/subscription.html -->
<div class="subscription-plans">
    <div class="plan free">
        <h3>Free</h3>
        <div class="price">₹0<span>/month</span></div>
        <ul>
            <li>5 queries per day</li>
            <li>Basic legal research</li>
            <li>Case law search (limited)</li>
            <li>Standard AI responses</li>
        </ul>
        <button class="current-plan">Current Plan</button>
    </div>
    
    <div class="plan premium">
        <h3>Premium</h3>
        <div class="price">₹999<span>/month</span></div>
        <ul>
            <li>Unlimited queries</li>
            <li>Document drafting (10/month)</li>
            <li>Document review (50/month)</li>
            <li>Conversation history</li>
            <li>Export responses</li>
            <li>Priority support</li>
        </ul>
        <button onclick="upgradeToPremium()">Upgrade</button>
    </div>
    
    <div class="plan professional">
        <h3>Professional</h3>
        <div class="price">₹4,999<span>/month</span></div>
        <ul>
            <li>Everything in Premium</li>
            <li>Unlimited documents</li>
            <li>Team collaboration</li>
            <li>API access</li>
            <li>White-label options</li>
            <li>Dedicated support</li>
        </ul>
        <button onclick="upgradeToProfessional()">Upgrade</button>
    </div>
</div>
```

### **4.2 Usage Dashboard**

```html
<!-- Show usage limits and current usage -->
<div class="usage-dashboard">
    <h3>Your Usage This Month</h3>
    <div class="usage-item">
        <span>Queries</span>
        <div class="progress-bar">
            <div class="progress" style="width: 60%"></div>
        </div>
        <span>30 / Unlimited</span>
    </div>
    <div class="usage-item">
        <span>Document Reviews</span>
        <div class="progress-bar">
            <div class="progress" style="width: 80%"></div>
        </div>
        <span>40 / 50</span>
        <button onclick="upgrade()">Upgrade for Unlimited</button>
    </div>
</div>
```

---

## **Phase 5: API Development (Professional Tier)**

### **5.1 API Authentication**

```python
# backend/app/api/api_keys.py

@router.post("/api-keys")
async def create_api_key(user: User = Depends(get_current_user)):
    """Create API key for Professional tier users"""
    if user.subscription_tier != 'professional':
        raise HTTPException(403, "API access requires Professional tier")
    
    api_key = generate_api_key()
    await APIKey.create(user_id=user.id, key=api_key)
    return {"api_key": api_key}

@router.get("/api/v2/research")
async def api_research(query: str, api_key: str = Header(...)):
    """API endpoint for research queries"""
    user = await verify_api_key(api_key)
    # Check API rate limits
    # Process query
    # Return response
```

---

## **Files to Create/Modify**

### **New Backend Files:**
1. `backend/app/models/user.py` - User model
2. `backend/app/models/subscription.py` - Subscription model
3. `backend/app/models/usage.py` - Usage tracking models
4. `backend/app/api/auth.py` - Authentication endpoints
5. `backend/app/api/subscriptions.py` - Subscription management
6. `backend/app/services/payment.py` - Payment processing
7. `backend/app/services/usage_tracking.py` - Usage tracking service
8. `backend/app/middleware/auth.py` - Authentication middleware
9. `backend/app/middleware/rate_limiter.py` - Rate limiting
10. `backend/app/core/database.py` - Database configuration (PostgreSQL/SQLite)

### **Modified Backend Files:**
1. `backend/app/api/legal_research.py` - Add usage tracking
2. `backend/app/api/document_drafting.py` - Add tier checks
3. `backend/app/api/document_review.py` - Add tier checks
4. `backend/app/main.py` - Add new routers

### **New Frontend Files:**
1. `frontend/subscription.html` - Subscription management page
2. `frontend/dashboard.html` - User dashboard with usage stats
3. `frontend/auth.html` - Login/Register pages
4. `frontend/js/subscription.js` - Subscription management logic

### **Modified Frontend Files:**
1. `frontend/index.html` - Add authentication checks, usage limits UI, upgrade prompts

---

## **Environment Variables to Add**

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/legalmitra
# or SQLite for development:
# DATABASE_URL=sqlite:///./legalmitra.db

# Payment Gateway (Razorpay)
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret

# JWT for authentication
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Email (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# File Storage (for documents)
STORAGE_TYPE=local  # or s3, azure
STORAGE_PATH=./storage
# or for cloud:
# AWS_ACCESS_KEY_ID=...
# AWS_SECRET_ACCESS_KEY=...
# S3_BUCKET_NAME=legalmitra-documents
```

---

## **Database Migration Strategy**

Use Alembic for database migrations:

```bash
# Install Alembic
pip install alembic

# Initialize
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add user and subscription tables"

# Apply migration
alembic upgrade head
```

---

This implementation plan provides a clear roadmap for adding monetization features to LegalMitra while maintaining the existing functionality for free users.

