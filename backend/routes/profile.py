from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from ..database import supabase
from ..models import UserUpdate, MessageResponse
from ..middleware.auth import get_current_user
from ..services.storage import upload_file
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/me")
async def get_my_profile(current_user = Depends(get_current_user)):
    """Get current user's profile"""
    user = supabase.table("users")\
        .select("*, parish:parish_id(name)")\
        .eq("id", current_user['id'])\
        .single()\
        .execute()
    
    if not user.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.data

@router.put("/me")
async def update_profile(
    updates: UserUpdate,
    current_user = Depends(get_current_user)
):
    """Update user profile"""
    update_data = updates.dict(exclude_unset=True)
    if update_data:
        result = supabase.table("users")\
            .update(update_data)\
            .eq("id", current_user['id'])\
            .execute()
        return result.data[0]
    return current_user

@router.post("/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    """Upload profile avatar"""
    file_url = await upload_file(file, f"avatars/{current_user['id']}")
    
    supabase.table("users")\
        .update({"avatar_url": file_url})\
        .eq("id", current_user['id'])\
        .execute()
    
    return {"avatar_url": file_url}

@router.get("/parish-members")
async def get_parish_members(current_user = Depends(get_current_user)):
    """Get members of current user's parish"""
    members = supabase.table("users")\
        .select("id, full_name, email, phone, role, avatar_url, last_seen")\
        .eq("parish_id", current_user['parish_id'])\
        .eq("is_active", True)\
        .order("role")\
        .execute()
    
    return members.data

@router.get("/users/search")
async def search_users(
    query: str,
    current_user = Depends(get_current_user)
):
    """Search users by name or email"""
    results = supabase.table("users")\
        .select("id, full_name, email, avatar_url, role, parish_id")\
        .ilike("full_name", f"%{query}%")\
        .limit(20)\
        .execute()
    
    return results.data
