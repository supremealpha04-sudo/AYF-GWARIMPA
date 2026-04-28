from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
import os
from typing import Optional
from ..database import supabase, get_user_by_email
from ..models import LoginRequest, UserCreate, TokenResponse, UserResponse, MessageResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid authentication token")

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    try:
        # Authenticate with Supabase
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        
        # Get user profile
        user_data = supabase.table("users")\
            .select("*")\
            .eq("email", request.email)\
            .execute()
        
        if not user_data.data:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        user = user_data.data[0]
        
        # Update last seen
        supabase.table("users").update({"last_seen": datetime.now().isoformat()}).eq("id", user["id"]).execute()
        
        # Create custom token
        access_token = create_access_token(data={"sub": user["id"], "email": user["email"], "role": user["role"]})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=response.session.refresh_token,
            user=UserResponse(**user)
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid email or password")

@router.post("/register", response_model=MessageResponse)
async def register(user: UserCreate):
    try:
        # Check if user exists
        existing = get_user_by_email(user.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create auth user
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "full_name": user.full_name,
                    "parish_id": user.parish_id
                }
            }
        })
        
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Failed to create user")
        
        # Create user profile
        user_data = {
            "id": auth_response.user.id,
            "email": user.email,
            "full_name": user.full_name,
            "parish_id": user.parish_id,
            "phone": user.phone,
            "role": "member"
        }
        
        supabase.table("users").insert(user_data).execute()
        
        return MessageResponse(message="User registered successfully", data={"user_id": auth_response.user.id})
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/logout", response_model=MessageResponse)
async def logout():
    try:
        supabase.auth.sign_out()
        return MessageResponse(message="Logged out successfully")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=UserResponse)
async def get_current_user(payload: dict = Depends(verify_token)):
    user = get_user_by_email(payload.get("email"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user)
