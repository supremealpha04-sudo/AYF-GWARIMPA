import sys
from pathlib import Path
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

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
        "*",  # Allow all for now
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# ROOT ENDPOINT - Landing Page (This fixes your issue!)
# =====================================================

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AYF Connect - Gwarimpa Archdeaconry</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #8B5CF6 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                max-width: 900px;
                width: 100%;
            }
            
            .card {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 24px;
                padding: 48px;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                backdrop-filter: blur(10px);
            }
            
            .logo {
                text-align: center;
                margin-bottom: 32px;
            }
            
            .logo-icon {
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 48px;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            }
            
            h1 {
                font-size: 32px;
                color: #1E3A8A;
                text-align: center;
                margin-bottom: 8px;
            }
            
            .subtitle {
                text-align: center;
                color: #6B7280;
                margin-bottom: 32px;
            }
            
            .status-badge {
                background: #10B981;
                color: white;
                padding: 6px 16px;
                border-radius: 50px;
                display: inline-block;
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 32px;
                text-align: center;
                width: 100%;
            }
            
            .endpoints-section {
                background: #F9FAFB;
                border-radius: 16px;
                padding: 24px;
                margin-top: 24px;
            }
            
            .endpoints-section h2 {
                color: #1F2937;
                font-size: 20px;
                margin-bottom: 16px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .endpoint-grid {
                display: grid;
                gap: 12px;
            }
            
            .endpoint {
                background: white;
                padding: 12px 16px;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 10px;
                border: 1px solid #E5E7EB;
                transition: all 0.3s ease;
            }
            
            .endpoint:hover {
                border-color: #3B82F6;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
            
            .endpoint-method {
                font-weight: 700;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 12px;
            }
            
            .method-get { background: #10B981; color: white; }
            .method-post { background: #3B82F6; color: white; }
            .method-put { background: #F59E0B; color: white; }
            .method-delete { background: #EF4444; color: white; }
            
            .endpoint-url {
                font-family: 'Courier New', monospace;
                font-size: 14px;
                color: #374151;
                flex: 1;
            }
            
            .endpoint-url a {
                color: #374151;
                text-decoration: none;
            }
            
            .endpoint-url a:hover {
                color: #3B82F6;
                text-decoration: underline;
            }
            
            .endpoint-desc {
                font-size: 12px;
                color: #6B7280;
            }
            
            .footer {
                text-align: center;
                margin-top: 32px;
                padding-top: 24px;
                border-top: 1px solid #E5E7EB;
                color: #6B7280;
                font-size: 14px;
            }
            
            @media (max-width: 640px) {
                .card { padding: 24px; }
                .endpoint { flex-direction: column; align-items: flex-start; }
                h1 { font-size: 24px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <div class="logo">
                    <div class="logo-icon">⛪</div>
                </div>
                <h1>AYF Connect API</h1>
                <div class="subtitle">Gwarimpa Archdeaconry Youth Fellowship Platform</div>
                <div class="status-badge">✅ Backend API is Running</div>
                
                <div class="endpoints-section">
                    <h2>📡 Available API Endpoints</h2>
                    <div class="endpoint-grid">
                        <div class="endpoint">
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-url"><a href="/api/">/api/</a></span>
                            <span class="endpoint-desc">API root information</span>
                        </div>
                        <div class="endpoint">
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-url"><a href="/api/health">/api/health</a></span>
                            <span class="endpoint-desc">Health check</span>
                        </div>
                        <div class="endpoint">
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-url"><a href="/api/test">/api/test</a></span>
                            <span class="endpoint-desc">Test endpoint</span>
                        </div>
                        <div class="endpoint">
                            <span class="endpoint-method method-post">POST</span>
                            <span class="endpoint-url">/api/auth/login</span>
                            <span class="endpoint-desc">User login</span>
                        </div>
                        <div class="endpoint">
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-url"><a href="/api/calendar/events?month=4&year=2026">/api/calendar/events?month=4&year=2026</a></span>
                            <span class="endpoint-desc">Get calendar events</span>
                        </div>
                        <div class="endpoint">
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-url"><a href="/api/feed/posts">/api/feed/posts</a></span>
                            <span class="endpoint-desc">Get feed posts</span>
                        </div>
                        <div class="endpoint">
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-url"><a href="/api/chat/groups">/api/chat/groups</a></span>
                            <span class="endpoint-desc">Get chat groups</span>
                        </div>
                        <div class="endpoint">
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-url"><a href="/api/quarterly/shares">/api/quarterly/shares</a></span>
                            <span class="endpoint-desc">Get quarterly shares</span>
                        </div>
                        <div class="endpoint">
                            <span class="endpoint-method method-get">GET</span>
                            <span class="endpoint-url"><a href="/api/profile/me">/api/profile/me</a></span>
                            <span class="endpoint-desc">Get user profile</span>
                        </div>
                    </div>
                </div>
                
                <div class="footer">
                    <p>🎉 Your API is successfully deployed!</p>
                    <p style="margin-top: 8px; font-size: 12px;">Your React frontend will be displayed here once built.</p>
                    <p style="margin-top: 8px;">📅 Last updated: April 28, 2026</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

# =====================================================
# API ROOT ENDPOINT
# =====================================================

@app.get("/api/")
async def api_root():
    return {
        "message": "AYF Connect API",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs",
        "endpoints": {
            "health": "/api/health",
            "test": "/api/test",
            "calendar": "/api/calendar/events?month=4&year=2026",
            "feed": "/api/feed/posts",
            "chat": "/api/chat/groups",
            "quarterly": "/api/quarterly/shares",
            "auth_login": "/api/auth/login (POST)",
            "auth_me": "/api/auth/me",
            "profile": "/api/profile/me"
        }
    }

# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "message": "AYF Connect API is running",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/test")
async def test():
    return {"message": "Test endpoint working!", "timestamp": datetime.now().isoformat()}

# =====================================================
# AUTH MODELS
# =====================================================

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    avatar_url: Optional[str] = None
    is_active: bool = True

# =====================================================
# AUTH ENDPOINTS
# =====================================================

@app.post("/api/auth/login")
async def login(request: LoginRequest):
    return {
        "access_token": "mock_token_" + datetime.now().strftime("%Y%m%d%H%M%S"),
        "refresh_token": "mock_refresh_" + datetime.now().strftime("%Y%m%d%H%M%S"),
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
        "email": "user@ayfgwarimpa.org",
        "full_name": "John Doe",
        "role": "member",
        "parish_id": "1",
        "avatar_url": None,
        "is_active": True,
        "last_seen": datetime.now().isoformat()
    }

# =====================================================
# CALENDAR ENDPOINTS
# =====================================================

@app.get("/api/calendar/events")
async def get_calendar_events(month: int, year: int):
    events = []
    
    # Sample events for the requested month
    sample_events = [
        {"day": 1, "title": "New Month Thanksgiving", "level": "archdeaconry"},
        {"day": 7, "title": "Youth Fellowship", "level": "diocese"},
        {"day": 14, "title": "Parish Meeting", "level": "parish"},
        {"day": 21, "title": "Bible Study", "level": "archdeaconry"},
        {"day": 28, "title": "Combined Service", "level": "diocese"},
    ]
    
    for event in sample_events:
        events.append({
            "id": f"{year}{month:02d}{event['day']}",
            "title": event['title'],
            "display_text": f"{'DIOCESE: ' if event['level'] == 'diocese' else ''}{event['title']}",
            "event_date": f"{year}-{month:02d}-{event['day']:02d}",
            "event_level": event['level'],
            "description": f"{event['title']} - A time of fellowship and worship",
            "created_at": datetime.now().isoformat()
        })
    
    return events

# =====================================================
# FEED ENDPOINTS
# =====================================================

@app.get("/api/feed/posts")
async def get_feed_posts(limit: int = 20):
    return [
        {
            "id": "1",
            "title": "Welcome to AYF Connect!",
            "content": "Welcome to AYF Connect! This is your new fellowship platform for Gwarimpa Archdeaconry. Stay connected with events, announcements, and fellow members.",
            "post_type": "announcement",
            "author": {
                "id": "admin1",
                "full_name": "AYF Admin",
                "avatar_url": None,
                "role": "admin"
            },
            "created_at": datetime.now().isoformat(),
            "likes": [{"count": 15}],
            "comments": [{"count": 3}],
            "share_count": 5,
            "view_count": 127,
            "user_liked": False,
            "media_urls": [],
            "media_types": []
        },
        {
            "id": "2",
            "title": "Weekly Prayer Meeting",
            "content": "Join us every Friday at 6pm for our weekly prayer meeting. Come with a heart of worship!",
            "post_type": "event",
            "author": {
                "id": "2",
                "full_name": "Prayer Coordinator",
                "avatar_url": None,
                "role": "parish_sec"
            },
            "created_at": datetime.now().isoformat(),
            "likes": [{"count": 28}],
            "comments": [{"count": 7}],
            "share_count": 12,
            "view_count": 245,
            "user_liked": True,
            "media_urls": [],
            "media_types": []
        }
    ]

@app.post("/api/feed/posts")
async def create_post():
    return {"message": "Post created successfully", "post_id": f"post_{int(datetime.now().timestamp())}"}

@app.post("/api/feed/posts/{post_id}/like")
async def like_post(post_id: str):
    return {"message": f"Post {post_id} liked", "liked": True}

@app.post("/api/feed/posts/{post_id}/comment")
async def comment_on_post(post_id: str, comment: str = None):
    return {"message": f"Comment added to post {post_id}", "comment_id": f"comment_{int(datetime.now().timestamp())}"}

@app.post("/api/feed/posts/{post_id}/share")
async def share_post(post_id: str):
    return {"message": f"Post {post_id} shared", "share_count": 9}

# =====================================================
# CHAT ENDPOINTS
# =====================================================

@app.get("/api/chat/groups")
async def get_chat_groups():
    return [
        {
            "id": "general_1",
            "name": "General Fellowship",
            "group_type": "general",
            "description": "All members chat - Stay connected with everyone",
            "unread_count": 0,
            "last_message": "Welcome everyone to AYF Connect!",
            "last_message_time": datetime.now().isoformat(),
            "member_count": 45
        },
        {
            "id": "parish_1",
            "name": "St. John's Parish Group",
            "group_type": "parish",
            "description": "St. John's Parish members only",
            "unread_count": 3,
            "last_message": "Prayer meeting today at 6pm",
            "last_message_time": datetime.now().isoformat(),
            "member_count": 12
        },
        {
            "id": "presidents_1",
            "name": "Presidents Council",
            "group_type": "presidents",
            "description": "Archdeaconry and Parish Presidents only",
            "unread_count": 1,
            "last_message": "Meeting on Saturday at 10am",
            "last_message_time": datetime.now().isoformat(),
            "member_count": 11
        }
    ]

@app.get("/api/chat/messages/{group_id}")
async def get_messages(group_id: str, limit: int = 50):
    return [
        {
            "id": "1",
            "message": "Hello everyone! Welcome to AYF Connect!",
            "sender": {"id": "admin1", "full_name": "Admin", "avatar_url": None},
            "created_at": datetime.now().isoformat(),
            "file_url": None,
            "voice_note_url": None
        },
        {
            "id": "2",
            "message": "Thank you! Glad to be part of this platform.",
            "sender": {"id": "user1", "full_name": "Member", "avatar_url": None},
            "created_at": datetime.now().isoformat(),
            "file_url": None,
            "voice_note_url": None
        }
    ]

@app.post("/api/chat/messages")
async def send_message():
    return {"message": "Message sent", "message_id": f"msg_{int(datetime.now().timestamp())}"}

@app.get("/api/chat/conversations")
async def get_conversations():
    return [
        {
            "id": "conv_1",
            "user": {
                "id": "user2",
                "full_name": "John Smith",
                "avatar_url": None,
                "role": "parish_president"
            },
            "last_message": "See you at the meeting",
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
    return {"message": "Private message sent", "message_id": f"priv_{int(datetime.now().timestamp())}"}

# =====================================================
# QUARTERLY SHARES ENDPOINTS
# =====================================================

@app.get("/api/quarterly/shares")
async def get_quarterly_shares():
    return [
        {
            "id": "1",
            "title": "Q1 2026 Evangelism Fund",
            "description": "Support for community outreach programs. Each parish is expected to contribute N50,000 for evangelism materials and logistics.",
            "quarter": 1,
            "year": 2026,
            "file_url": None,
            "file_name": None,
            "created_at": "2026-01-15T10:00:00",
            "forwarded": False
        },
        {
            "id": "2",
            "title": "Q2 2026 Building Fund",
            "description": "Church building maintenance and renovation project. Target: N100,000 per parish to be completed by end of Q2.",
            "quarter": 2,
            "year": 2026,
            "file_url": None,
            "file_name": None,
            "created_at": "2026-04-01T09:00:00",
            "forwarded": True,
            "forwarded_at": "2026-04-02T14:30:00"
        },
        {
            "id": "3",
            "title": "Q3 2026 Youth Conference",
            "description": "Annual youth conference preparation. Each parish to send 10 representatives.",
            "quarter": 3,
            "year": 2026,
            "file_url": None,
            "file_name": None,
            "created_at": "2026-04-15T11:00:00",
            "forwarded": False
        }
    ]

@app.post("/api/quarterly/share/{share_id}/forward")
async def forward_share(share_id: str):
    return {"message": f"Share {share_id} forwarded to parish group", "forwarded": True, "forwarded_at": datetime.now().isoformat()}

# =====================================================
# PROFILE ENDPOINTS
# =====================================================

@app.get("/api/profile/me")
async def get_profile():
    return {
        "id": "1",
        "full_name": "John Doe",
        "email": "john.doe@ayfgwarimpa.org",
        "role": "member",
        "parish": {
            "id": "1",
            "name": "St. John's Anglican Church",
            "slug": "st-john"
        },
        "phone": "+234 812 345 6789",
        "avatar_url": None,
        "bio": "A committed member of AYF, passionate about youth development and church growth.",
        "created_at": "2026-01-01T00:00:00",
        "last_seen": datetime.now().isoformat(),
        "is_active": True
    }

@app.get("/api/profile/parish-members")
async def get_parish_members():
    return [
        {"id": "1", "full_name": "John Doe", "email": "john@example.com", "role": "member", "avatar_url": None, "last_seen": datetime.now().isoformat()},
        {"id": "2", "full_name": "Jane Smith", "email": "jane@example.com", "role": "member", "avatar_url": None, "last_seen": datetime.now().isoformat()},
        {"id": "3", "full_name": "Pastor Mike", "email": "pastor@example.com", "role": "parish_president", "avatar_url": None, "last_seen": datetime.now().isoformat()},
        {"id": "4", "full_name": "Sister Sarah", "email": "sarah@example.com", "role": "parish_sec", "avatar_url": None, "last_seen": datetime.now().isoformat()}
    ]

@app.put("/api/profile/me")
async def update_profile():
    return {"message": "Profile updated successfully", "updated_at": datetime.now().isoformat()}

@app.post("/api/profile/me/avatar")
async def upload_avatar():
    return {"message": "Avatar uploaded successfully", "avatar_url": "https://via.placeholder.com/150"}

# =====================================================
# ADMIN ENDPOINTS
# =====================================================

@app.get("/api/admin/users")
async def get_users():
    return [
        {"id": "1", "full_name": "Admin User", "email": "admin@ayf.org", "role": "admin", "is_active": True, "last_login": datetime.now().isoformat()},
        {"id": "2", "full_name": "Gen President", "email": "president@ayf.org", "role": "gen_president", "is_active": True, "last_login": datetime.now().isoformat()},
        {"id": "3", "full_name": "Parish President", "email": "pp@stjohn.org", "role": "parish_president", "is_active": True, "last_login": datetime.now().isoformat()},
        {"id": "4", "full_name": "Inactive User", "email": "inactive@example.com", "role": "member", "is_active": False, "last_login": "2026-01-01T00:00:00"}
    ]

@app.put("/api/admin/users/{user_id}/role")
async def assign_role(user_id: str, role: str = None):
    return {"message": f"User {user_id} role updated to {role}", "updated_at": datetime.now().isoformat()}

@app.put("/api/admin/users/{user_id}/activate")
async def activate_user(user_id: str):
    return {"message": f"User {user_id} activation status toggled", "updated_at": datetime.now().isoformat()}

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
            "tip": "Try adding /api/ to your URL or check the available endpoints at /api/",
            "available_endpoints": [
                "/",
                "/api/",
                "/api/health",
                "/api/test",
                "/api/auth/login (POST)",
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
