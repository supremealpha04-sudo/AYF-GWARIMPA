from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    GEN_PRESIDENT = "gen_president"
    GEN_SEC = "gen_sec"
    PARISH_PRESIDENT = "parish_president"
    PARISH_SEC = "parish_sec"
    PROVOST = "provost"
    PRO = "pro"
    VICE_PRESIDENT = "vice_president"
    MEMBER = "member"

class EventLevel(str, Enum):
    ARCHDEACONRY = "archdeaconry"
    DIOCESE = "diocese"
    PARISH = "parish"

class PostType(str, Enum):
    ANNOUNCEMENT = "announcement"
    EVENT = "event"
    NOTICE = "notice"
    TESTIMONY = "testimony"

# Auth Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    parish_id: str
    phone: Optional[str] = None

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    parish_id: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    parish_id: Optional[str]
    role: str
    avatar_url: Optional[str]
    phone: Optional[str]
    is_active: bool
    last_seen: Optional[datetime]
    created_at: datetime

# Calendar Models
class YearlyEventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    event_date: date
    event_level: EventLevel
    parish_id: Optional[str] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = Field(None, pattern="^(weekly|monthly|yearly)$")
    recurrence_end_date: Optional[date] = None

class YearlyEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[date] = None
    event_level: Optional[EventLevel] = None

# Quarterly Share Models
class QuarterlyShareCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    quarter: int = Field(..., ge=1, le=4)
    year: int = Field(..., ge=2024, le=2030)

# Feed Models
class FeedPostCreate(BaseModel):
    title: Optional[str] = None
    content: str = Field(..., min_length=1)
    post_type: PostType = PostType.ANNOUNCEMENT
    media_urls: Optional[List[str]] = None
    media_types: Optional[List[str]] = None

class CommentCreate(BaseModel):
    comment: str = Field(..., min_length=1, max_length=500)

# Chat Models
class ChatMessageCreate(BaseModel):
    group_id: Optional[str] = None
    message: Optional[str] = None
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    voice_note_url: Optional[str] = None
    voice_note_duration: Optional[int] = Field(None, ge=1, le=300)
    reply_to: Optional[str] = None

class PrivateMessageCreate(BaseModel):
    receiver_id: str
    message: Optional[str] = None
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    voice_note_url: Optional[str] = None
    voice_note_duration: Optional[int] = Field(None, ge=1, le=300)

# Notification Models
class NotificationCreate(BaseModel):
    user_id: str
    type: str
    title: str
    message: str
    data: Optional[dict] = None

# Response Models
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse

class MessageResponse(BaseModel):
    message: str
    data: Optional[dict] = None
