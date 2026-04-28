from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import Optional
from ..database import supabase
from ..models import QuarterlyShareCreate, MessageResponse
from ..middleware.auth import get_current_user, require_role, get_parish_president
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quarterly", tags=["Quarterly Shares"])

@router.post("/share", response_model=MessageResponse)
async def create_quarterly_share(
    share_data: QuarterlyShareCreate,
    current_user = Depends(require_role(["admin", "gen_president", "gen_sec"]))
):
    """Admin only - create quarterly share"""
    
    share = {
        "title": share_data.title,
        "description": share_data.description,
        "quarter": share_data.quarter,
        "year": share_data.year,
        "created_by": current_user['id']
    }
    
    result = supabase.table("quarterly_shares").insert(share).execute()
    share_id = result.data[0]['id']
    
    # Notify all parish presidents
    presidents = supabase.table("users")\
        .select("id")\
        .eq("role", "parish_president")\
        .eq("is_active", True)\
        .execute()
    
    for pres in presidents.data:
        supabase.table("notifications").insert({
            "user_id": pres['id'],
            "type": "quarterly_share",
            "title": "New Quarterly Share",
            "message": f"Q{share_data.quarter} {share_data.year}: {share_data.title}",
            "data": {"share_id": share_id}
        }).execute()
    
    return MessageResponse(message="Quarterly share created", data={"share_id": share_id})

@router.post("/share/{share_id}/upload")
async def upload_share_file(
    share_id: str,
    file: UploadFile = File(...),
    current_user = Depends(require_role(["admin", "gen_president"]))
):
    """Upload file for quarterly share"""
    from ..services.storage import upload_file
    
    file_url = await upload_file(file, f"quarterly/{share_id}")
    
    supabase.table("quarterly_shares").update({
        "file_url": file_url,
        "file_name": file.filename
    }).eq("id", share_id).execute()
    
    return {"file_url": file_url}

@router.get("/shares")
async def get_quarterly_shares(current_user = Depends(get_current_user)):
    """Get quarterly shares - presidents see all, members see only forwarded ones"""
    if current_user['role'] in ['parish_president', 'admin', 'gen_president', 'gen_sec']:
        # Presidents and admins see all shares
        result = supabase.table("quarterly_shares")\
            .select("*")\
            .order("year", desc=True)\
            .order("quarter", desc=True)\
            .execute()
        
        # Track view for presidents
        if current_user['role'] == 'parish_president':
            for share in result.data:
                supabase.table("quarterly_share_views").upsert({
                    "share_id": share['id'],
                    "parish_president_id": current_user['id'],
                    "viewed_at": datetime.now().isoformat()
                }, on_conflict="share_id,parish_president_id").execute()
        
        return result.data
    else:
        # Members see only shares forwarded to their parish
        # Get the parish president for this member's parish
        president = supabase.table("users")\
            .select("id")\
            .eq("parish_id", current_user['parish_id'])\
            .eq("role", "parish_president")\
            .single()\
            .execute()
        
        if not president.data:
            return []
        
        # Get shares forwarded by this president
        result = supabase.table("quarterly_share_views")\
            .select("share_id, quarterly_shares(*)")\
            .eq("parish_president_id", president.data['id'])\
            .not_.is_("forwarded_at", "null")\
            .execute()
        
        return [item['quarterly_shares'] for item in result.data if item.get('quarterly_shares')]

@router.post("/share/{share_id}/forward", response_model=MessageResponse)
async def forward_to_parish_group(
    share_id: str,
    current_user = Depends(get_parish_president)
):
    """Parish president forwards share to their parish group"""
    # Get share details
    share = supabase.table("quarterly_shares")\
        .select("*")\
        .eq("id", share_id)\
        .single()\
        .execute()
    
    if not share.data:
        raise HTTPException(status_code=404, detail="Share not found")
    
    # Get parish group
    group = supabase.table("chat_groups")\
        .select("id")\
        .eq("group_type", "parish")\
        .eq("parish_id", current_user['parish_id'])\
        .single()\
        .execute()
    
    if not group.data:
        raise HTTPException(status_code=404, detail="Parish group not found")
    
    # Create system message in parish chat
    message_text = f"""📢 **QUARTERLY SHARE FROM ARCHDEACONRY**

**Title:** {share.data['title']}
**Quarter:** Q{share.data['quarter']} {share.data['year']}

**Description:**
{share.data['description']}

{'📎 Download attachment: ' + share.data['file_url'] if share.data.get('file_url') else ''}
"""
    
    supabase.table("chat_messages").insert({
        "group_id": group.data['id'],
        "sender_id": current_user['id'],
        "message": message_text,
        "file_url": share.data.get('file_url')
    }).execute()
    
    # Update forward log
    supabase.table("quarterly_share_views")\
        .update({"forwarded_at": datetime.now().isoformat()})\
        .eq("share_id", share_id)\
        .eq("parish_president_id", current_user['id'])\
        .execute()
    
    return MessageResponse(message="Forwarded to parish group successfully")
