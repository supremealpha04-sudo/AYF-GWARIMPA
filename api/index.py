import sys
from pathlib import Path
import os

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Create app
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# ALL ROUTES MUST HAVE /api/ PREFIX
# =====================================================

@app.get("/api/")
async def root():
    return {
        "message": "AYF Connect API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "test": "/api/test",
            "calendar": "/api/calendar/events?month=4&year=2026",
            "feed": "/api/feed/posts",
            "chat": "/api/chat/groups",
            "quarterly": "/api/quarterly/shares",
            "auth": "/api/auth/login"
        }
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "message": "AYF Connect API is running",
        "timestamp": "2026-04-28"
    }

@app.get("/api/test")
async def test():
    return {"message": "Test endpoint working!"}

# =====================================================
# AUTH ENDPOINTS
# =====================================================

from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    # Temporary mock response
    return {
        "access_token": "mock_token_123",
        "user": {
            "id": "1",
            "email": request.email,
            "full_name": "Test User",
            "role": "member"
        }
    }

@app.get("/api/auth/me")
async def get_current_user():
    return {
        "id": "1",
        "email": "user@example.com",
        "full_name": "Test User",
        "role": "member"
    }

# =====================================================
# CALENDAR ENDPOINTS
# =====================================================

@app.get("/api/calendar/events")
async def get_calendar_events(month: int, year: int):
    return [
        {
            "id": "1",
            "title": "Sunday Service",
            "display_text": "Sunday Service",
            "event_date": f"{year}-{month:02d}-15",
            "event_level": "archdeaconry",
            "description": "Weekly Sunday worship service"
        },
        {
            "id": "2",
            "title": "Youth Fellowship",
            "display_text": "DIOCESE: Youth Fellowship",
            "event_date": f"{year}-{month:02d}-22",
            "event_level": "diocese",
            "description": "Monthly youth gathering"
        },
        {
            "id": "3",
            "title": "Parish Meeting",
            "display_text": "Parish Meeting",
            "event_date": f"{year}-{month:02d}-28",
            "event_level": "parish",
            "description": "Monthly parish meeting"
        }
    ]

# =====================================================
# FEED ENDPOINTS
# =====================================================

@app.get("/api/feed/posts")
async def get_feed_posts(limit: int = 20):
    return [
        {
            "id": "1",
            "content": "Welcome to AYF Connect! This is your new fellowship platform.",
            "post_type": "announcement",
            "author": {
                "full_name": "Admin AYF",
                "avatar_url": None
            },
            "created_at": "2026-04-28T10:00:00",
            "likes": [{"count": 5}],
            "comments": [{"count": 2}],
            "share_count": 3,
            "view_count": 45,
            "user_liked": False
        },
        {
            "id": "2",
            "content": "Prayer meeting this Friday at 6pm. All are invited!",
            "post_type": "event",
            "author": {
                "full_name": "Prayer Coordinator",
                "avatar_url": None
            },
            "created_at": "2026-04-27T15:30:00",
            "likes": [{"count": 12}],
            "comments": [{"count": 4}],
            "share_count": 7,
            "view_count": 89,
            "user_liked": True
        }
    ]

@app.post("/api/feed/posts")
async def create_post():
    return {"message": "Post created successfully"}

@app.post("/api/feed/posts/{post_id}/like")
async def like_post(post_id: str):
    return {"message": f"Post {post_id} liked"}

@app.post("/api/feed/posts/{post_id}/comment")
async def comment_on_post(post_id: str):
    return {"message": f"Comment added to post {post_id}"}

# =====================================================
# CHAT ENDPOINTS
# =====================================================

@app.get("/api/chat/groups")
async def get_chat_groups():
    return [
        {
            "id": "1",
            "name": "General Fellowship",
            "group_type": "general",
            "description": "All members chat"
        },
        {
            "id": "2",
            "name": "St. John's Group",
            "group_type": "parish",
            "description": "St. John's Parish"
        },
        {
            "id": "3",
            "name": "Presidents Council",
            "group_type": "presidents",
            "description": "Parish Presidents only"
        }
    ]

@app.get("/api/chat/messages/{group_id}")
async def get_messages(group_id: str, limit: int = 50):
    return [
        {
            "id": "1",
            "message": "Hello everyone!",
            "sender": {"full_name": "User 1", "avatar_url": None},
            "created_at": "2026-04-28T09:00:00"
        },
        {
            "id": "2",
            "message": "Welcome to the group!",
            "sender": {"full_name": "User 2", "avatar_url": None},
            "created_at": "2026-04-28T09:05:00"
        }
    ]

@app.post("/api/chat/messages")
async def send_message():
    return {"message": "Message sent"}

@app.get("/api/chat/conversations")
async def get_conversations():
    return []

@app.get("/api/chat/messages/private/{user_id}")
async def get_private_messages(user_id: str):
    return []

# =====================================================
# QUARTERLY SHARES ENDPOINTS
# =====================================================

@app.get("/api/quarterly/shares")
async def get_quarterly_shares():
    return [
        {
            "id": "1",
            "title": "Q1 Evangelism Fund",
            "description": "Support for community outreach programs",
            "quarter": 1,
            "year": 2026,
            "created_at": "2026-01-15T10:00:00"
        },
        {
            "id": "2",
            "title": "Q2 Building Fund",
            "description": "Church building maintenance",
            "quarter": 2,
            "year": 2026,
            "created_at": "2026-04-01T09:00:00"
        }
    ]

@app.post("/api/quarterly/share/{share_id}/forward")
async def forward_share(share_id: str):
    return {"message": f"Share {share_id} forwarded to parish"}

# =====================================================
# PROFILE ENDPOINTS
# =====================================================

@app.get("/api/profile/me")
async def get_profile():
    return {
        "id": "1",
        "full_name": "Test User",
        "email": "user@example.com",
        "role": "member",
        "parish": {"name": "St. John's Church"},
        "phone": "+1234567890",
        "created_at": "2026-01-01T00:00:00"
    }

@app.get("/api/profile/parish-members")
async def get_parish_members():
    return [
        {"id": "1", "full_name": "Member 1", "role": "member"},
        {"id": "2", "full_name": "Member 2", "role": "member"},
        {"id": "3", "full_name": "Parish President", "role": "parish_president"}
    ]

# =====================================================
# ADMIN ENDPOINTS
# =====================================================

@app.get("/api/admin/users")
async def get_users():
    return [
        {"id": "1", "full_name": "Admin User", "email": "admin@ayf.org", "role": "admin"},
        {"id": "2", "full_name": "Parish President", "email": "president@church.org", "role": "parish_president"}
    ]

@app.put("/api/admin/users/{user_id}/role")
async def assign_role(user_id: str):
    return {"message": f"Role updated for user {user_id}"}

# =====================================================
# ERROR HANDLER
# =====================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Endpoint not found",
            "path": str(request.url),
            "available_endpoints": [
                "/api/",
                "/api/health",
                "/api/test",
                "/api/auth/login",
                "/api/auth/me",
                "/api/calendar/events?month=4&year=2026",
                "/api/feed/posts",
                "/api/chat/groups",
                "/api/quarterly/shares",
                "/api/profile/me"
            ]
        }
    )

# =====================================================
# VERCEL HANDLER
# =====================================================
handler = app
