import sys
from pathlib import Path
import os

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Create app
app = FastAPI()

# CORS - Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ayf-gwarimpa.vercel.app",
        "https://ayf-gwarimpa-cl32u1h7d-supremealpha04-sudos-projects.vercel.app",
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# FRONTEND SERVING (for production)
# =====================================================

# Check if frontend dist exists
frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"

@app.get("/")
async def serve_root():
    """Serve frontend or API info"""
    index_file = frontend_dist / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "message": "AYF Connect API",
        "docs": "/api/",
        "endpoints": {
            "api_root": "/api/",
            "health": "/api/health",
            "calendar": "/api/calendar/events?month=4&year=2026",
            "feed": "/api/feed/posts",
            "chat": "/api/chat/groups"
        }
    }

# =====================================================
# API ENDPOINTS (ALL MUST START WITH /api/)
# =====================================================

@app.get("/api/")
async def api_root():
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
            "auth_login": "/api/auth/login",
            "auth_me": "/api/auth/me",
            "profile": "/api/profile/me"
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
    return {"message": "API test endpoint working!"}

# =====================================================
# AUTH ENDPOINTS
# =====================================================

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    # Mock login - replace with actual auth
    return {
        "access_token": "mock_token_123",
        "refresh_token": "mock_refresh_456",
        "user": {
            "id": "1",
            "email": request.email,
            "full_name": "Test User",
            "role": "member",
            "avatar_url": None,
            "is_active": True
        }
    }

@app.get("/api/auth/me")
async def get_current_user():
    return {
        "id": "1",
        "email": "user@example.com",
        "full_name": "Test User",
        "role": "member",
        "parish_id": "1",
        "avatar_url": None,
        "is_active": True
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
            "description": "Weekly Sunday worship service",
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "2",
            "title": "Youth Fellowship",
            "display_text": "DIOCESE: Youth Fellowship",
            "event_date": f"{year}-{month:02d}-22",
            "event_level": "diocese",
            "description": "Monthly youth gathering",
            "created_at": datetime.now().isoformat()
        },
        {
            "id": "3",
            "title": "Parish Meeting",
            "display_text": "Parish Meeting",
            "event_date": f"{year}-{month:02d}-28",
            "event_level": "parish",
            "description": "Monthly parish meeting",
            "created_at": datetime.now().isoformat()
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
            "title": "Welcome to AYF Connect!",
            "content": "Welcome to AYF Connect! This is your new fellowship platform for Gwarimpa Archdeaconry.",
            "post_type": "announcement",
            "author": {
                "id": "1",
                "full_name": "Admin AYF",
                "avatar_url": None,
                "role": "admin"
            },
            "created_at": datetime.now().isoformat(),
            "likes": [{"count": 5}],
            "comments": [{"count": 2}],
            "share_count": 3,
            "view_count": 45,
            "user_liked": False,
            "media_urls": [],
            "media_types": []
        },
        {
            "id": "2",
            "title": "Prayer Meeting",
            "content": "Prayer meeting this Friday at 6pm at the church hall. All are invited!",
            "post_type": "event",
            "author": {
                "id": "2",
                "full_name": "Prayer Coordinator",
                "avatar_url": None,
                "role": "parish_sec"
            },
            "created_at": datetime.now().isoformat(),
            "likes": [{"count": 12}],
            "comments": [{"count": 4}],
            "share_count": 7,
            "view_count": 89,
            "user_liked": True,
            "media_urls": [],
            "media_types": []
        }
    ]

@app.post("/api/feed/posts")
async def create_post():
    return {"message": "Post created successfully", "post_id": "new_123"}

@app.post("/api/feed/posts/{post_id}/like")
async def like_post(post_id: str):
    return {"message": f"Post {post_id} liked", "liked": True}

@app.post("/api/feed/posts/{post_id}/comment")
async def comment_on_post(post_id: str):
    return {"message": f"Comment added to post {post_id}", "comment_id": "comment_123"}

@app.post("/api/feed/posts/{post_id}/share")
async def share_post(post_id: str):
    return {"message": f"Post {post_id} shared", "share_count": 8}

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
            "description": "All members chat",
            "unread_count": 0,
            "last_message": "Welcome everyone!"
        },
        {
            "id": "2",
            "name": "St. John's Group",
            "group_type": "parish",
            "description": "St. John's Parish",
            "unread_count": 3,
            "last_message": "Prayer meeting today"
        },
        {
            "id": "3",
            "name": "Presidents Council",
            "group_type": "presidents",
            "description": "Parish Presidents only",
            "unread_count": 1,
            "last_message": "Meeting on Saturday"
        }
    ]

@app.get("/api/chat/messages/{group_id}")
async def get_messages(group_id: str, limit: int = 50):
    return [
        {
            "id": "1",
            "message": "Hello everyone! Welcome to AYF Connect.",
            "sender": {
                "id": "1",
                "full_name": "Admin",
                "avatar_url": None
            },
            "created_at": datetime.now().isoformat(),
            "file_url": None,
            "voice_note_url": None
        },
        {
            "id": "2",
            "message": "Thank you! Glad to be here.",
            "sender": {
                "id": "2",
                "full_name": "Member",
                "avatar_url": None
            },
            "created_at": datetime.now().isoformat(),
            "file_url": None,
            "voice_note_url": None
        }
    ]

@app.post("/api/chat/messages")
async def send_message():
    return {"message": "Message sent", "message_id": "msg_123"}

@app.get("/api/chat/conversations")
async def get_conversations():
    return [
        {
            "id": "conv_1",
            "user": {
                "id": "3",
                "full_name": "John Doe",
                "avatar_url": None,
                "role": "member"
            },
            "last_message": "See you at church",
            "last_message_time": datetime.now().isoformat(),
            "unread_count": 2
        }
    ]

@app.get("/api/chat/messages/private/{user_id}")
async def get_private_messages(user_id: str, limit: int = 50):
    return [
        {
            "id": "1",
            "message": "Hello, how are you?",
            "sender_id": user_id,
            "receiver_id": "1",
            "created_at": datetime.now().isoformat(),
            "is_read": True
        }
    ]

@app.post("/api/chat/messages/private")
async def send_private_message():
    return {"message": "Private message sent"}

# =====================================================
# QUARTERLY SHARES ENDPOINTS
# =====================================================

@app.get("/api/quarterly/shares")
async def get_quarterly_shares():
    return [
        {
            "id": "1",
            "title": "Q1 Evangelism Fund",
            "description": "Support for community outreach programs. Each parish is expected to contribute N50,000.",
            "quarter": 1,
            "year": 2026,
            "file_url": None,
            "file_name": None,
            "created_at": "2026-01-15T10:00:00",
            "forwarded": False
        },
        {
            "id": "2",
            "title": "Q2 Building Fund",
            "description": "Church building maintenance and renovation. Target: N100,000 per parish.",
            "quarter": 2,
            "year": 2026,
            "file_url": None,
            "file_name": None,
            "created_at": "2026-04-01T09:00:00",
            "forwarded": True,
            "forwarded_at": "2026-04-02T14:30:00"
        }
    ]

@app.post("/api/quarterly/share/{share_id}/forward")
async def forward_share(share_id: str):
    return {"message": f"Share {share_id} forwarded to parish group", "forwarded": True}

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
        "parish": {
            "id": "1",
            "name": "St. John's Church"
        },
        "phone": "+2341234567890",
        "avatar_url": None,
        "bio": "A committed member of AYF",
        "created_at": "2026-01-01T00:00:00",
        "last_seen": datetime.now().isoformat()
    }

@app.get("/api/profile/parish-members")
async def get_parish_members():
    return [
        {"id": "1", "full_name": "Member One", "email": "member1@example.com", "role": "member", "avatar_url": None},
        {"id": "2", "full_name": "Member Two", "email": "member2@example.com", "role": "member", "avatar_url": None},
        {"id": "3", "full_name": "Parish President", "email": "president@example.com", "role": "parish_president", "avatar_url": None}
    ]

@app.put("/api/profile/me")
async def update_profile():
    return {"message": "Profile updated successfully"}

# =====================================================
# ADMIN ENDPOINTS
# =====================================================

@app.get("/api/admin/users")
async def get_users():
    return [
        {"id": "1", "full_name": "Admin User", "email": "admin@ayf.org", "role": "admin", "is_active": True},
        {"id": "2", "full_name": "Gen President", "email": "president@ayf.org", "role": "gen_president", "is_active": True},
        {"id": "3", "full_name": "Parish President", "email": "pp@church.org", "role": "parish_president", "is_active": True}
    ]

@app.put("/api/admin/users/{user_id}/role")
async def assign_role(user_id: str, role: str = None):
    return {"message": f"User {user_id} role updated to {role}"}

# =====================================================
# ERROR HANDLERS
# =====================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Endpoint not found",
            "path": str(request.url),
            "tip": "Try adding /api/ to your URL",
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
