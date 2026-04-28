from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from typing import List, Optional
from ..database import get_user_by_email

security = HTTPBearer()
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this")
ALGORITHM = "HS256"

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid authentication token")

async def get_current_user(payload: dict = Depends(verify_token)):
    user = get_user_by_email(payload.get("email"))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="Account deactivated")
    return user

def require_role(roles: List[str]):
    async def role_checker(current_user = Depends(get_current_user)):
        if current_user['role'] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role required: {', '.join(roles)}"
            )
        return current_user
    return role_checker

async def get_parish_president(current_user = Depends(get_current_user)):
    if current_user['role'] != 'parish_president':
        raise HTTPException(status_code=403, detail="Parish president role required")
    return current_user

async def verify_websocket(token: str):
    """Verify WebSocket connection token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = get_user_by_email(payload.get("email"))
        if not user:
            raise ValueError("User not found")
        return user
    except jwt.PyJWTError:
        raise ValueError("Invalid token")
