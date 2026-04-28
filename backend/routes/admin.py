from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..database import supabase
from ..models import UserRole, MessageResponse
from ..middleware.auth import get_current_user, require_role
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
async def get_all_users(
    role: Optional[UserRole] = None,
    current_user = Depends(require_role(["admin", "gen_president"]))
):
    """Get all users (Admin only)"""
    query = supabase.table("users")\
        .select("*, parish:parish_id(name)")\
        .order("created_at", desc=True)
    
    if role:
        query = query.eq("role", role)
    
    result = query.execute()
    return result.data

@router.put("/users/{user_id}/role")
async def assign_role(
    user_id: str,
    role: UserRole,
    current_user = Depends(require_role(["admin"]))
):
    """Assign role to user (Admin only)"""
    # Check if user exists
    user = supabase.table("users").select("id").eq("id", user_id).single().execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update role
    result = supabase.table("users")\
        .update({"role": role})\
        .eq("id", user_id)\
        .execute()
    
    return MessageResponse(message=f"Role updated to {role}", data=result.data[0])

@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: str,
    current_user = Depends(require_role(["admin"]))
):
    """Activate or deactivate user"""
    user = supabase.table("users").select("is_active").eq("id", user_id).single().execute()
    if not user.data:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_status = not user.data['is_active']
    result = supabase.table("users")\
        .update({"is_active": new_status})\
        .eq("id", user_id)\
        .execute()
    
    return MessageResponse(message=f"User {'activated' if new_status else 'deactivated'}")
