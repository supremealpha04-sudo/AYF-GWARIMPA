from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from typing import List, Dict
from ..database import supabase
from ..models import ChatMessageCreate, PrivateMessageCreate, MessageResponse
from ..middleware.auth import get_current_user, verify_websocket
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["Chat"])

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, group_id: str = None):
        await websocket.accept()
        key = f"user_{user_id}"
        if key not in self.active_connections:
            self.active_connections[key] = []
        self.active_connections[key].append(websocket)
        
        # Also track by group if provided
        if group_id:
            group_key = f"group_{group_id}"
            if group_key not in self.active_connections:
                self.active_connections[group_key] = []
            self.active_connections[group_key].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: str):
        key = f"user_{user_id}"
        if key in self.active_connections:
            self.active_connections[key].remove(websocket)
    
    async def send_personal_message(self, message: dict, user_id: str):
        key = f"user_{user_id}"
        if key in self.active_connections:
            for connection in self.active_connections[key]:
                await connection.send_json(message)
    
    async def broadcast_to_group(self, message: dict, group_id: str):
        key = f"group_{group_id}"
        if key in self.active_connections:
            for connection in self.active_connections[key]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.get("/groups")
async def get_user_groups(current_user = Depends(get_current_user)):
    """Get chat groups for current user"""
    groups = []
    
    # Add general group
    general = supabase.table("chat_groups")\
        .select("*")\
        .eq("group_type", "general")\
        .single()\
        .execute()
    if general.data:
        groups.append(general.data)
    
    # Add parish group
    parish_group = supabase.table("chat_groups")\
        .select("*")\
        .eq("group_type", "parish")\
        .eq("parish_id", current_user['parish_id'])\
        .single()\
        .execute()
    if parish_group.data:
        groups.append(parish_group.data)
    
    # Add presidents group if applicable
    if current_user['role'] in ['parish_president', 'admin', 'gen_president']:
        presidents = supabase.table("chat_groups")\
            .select("*")\
            .eq("group_type", "presidents")\
            .single()\
            .execute()
        if presidents.data:
            groups.append(presidents.data)
    
    return groups

@router.get("/messages/{group_id}")
async def get_group_messages(
    group_id: str,
    limit: int = 50,
    before: str = None,
    current_user = Depends(get_current_user)
):
    """Get messages from a group"""
    # Verify user has access to this group
    group = supabase.table("chat_groups")\
        .select("*")\
        .eq("id", group_id)\
        .single()\
        .execute()
    
    if not group.data:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if group.data['group_type'] == 'parish':
        if group.data['parish_id'] != current_user['parish_id']:
            raise HTTPException(status_code=403, detail="Access denied")
    elif group.data['group_type'] == 'presidents':
        if current_user['role'] not in ['parish_president', 'admin', 'gen_president']:
            raise HTTPException(status_code=403, detail="Access denied")
    
    # Get messages
    query = supabase.table("chat_messages")\
        .select("*, sender:sender_id(full_name, avatar_url)")\
        .eq("group_id", group_id)\
        .order("created_at", desc=True)\
        .limit(limit)
    
    if before:
        query = query.lt("created_at", before)
    
    result = query.execute()
    
    return result.data[::-1]  # Return in ascending order

@router.post("/messages", response_model=MessageResponse)
async def send_message(
    message: ChatMessageCreate,
    current_user = Depends(get_current_user)
):
    """Send a message to a group"""
    message_data = {
        "group_id": message.group_id,
        "sender_id": current_user['id'],
        "message": message.message,
        "file_url": message.file_url,
        "file_type": message.file_type,
        "voice_note_url": message.voice_note_url,
        "voice_note_duration": message.voice_note_duration,
        "reply_to": message.reply_to
    }
    
    result = supabase.table("chat_messages").insert(message_data).execute()
    new_message = result.data[0]
    
    # Broadcast via WebSocket
    await manager.broadcast_to_group(new_message, message.group_id)
    
    return MessageResponse(message="Message sent", data=new_message)

@router.get("/conversations")
async def get_private_conversations(current_user = Depends(get_current_user)):
    """Get private conversations list"""
    conversations = supabase.table("private_conversations")\
        .select("*, user1:user1_id(full_name, avatar_url, id), user2:user2_id(full_name, avatar_url, id)")\
        .filter(f"or=(user1_id.eq.{current_user['id']},user2_id.eq.{current_user['id']})")\
        .execute()
    
    # Get last message for each conversation
    for conv in conversations.data:
        last_msg = supabase.table("private_messages")\
            .select("*")\
            .eq("conversation_id", conv['id'])\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()
        
        conv['last_message'] = last_msg.data[0] if last_msg.data else None
        
        # Get unread count
        unread = supabase.table("private_messages")\
            .select("count")\
            .eq("conversation_id", conv['id'])\
            .eq("receiver_id", current_user['id'])\
            .eq("is_read", False)\
            .execute()
        
        conv['unread_count'] = unread.data[0]['count'] if unread.data else 0
    
    return conversations.data

@router.get("/messages/private/{user_id}")
async def get_private_messages(
    user_id: str,
    limit: int = 50,
    current_user = Depends(get_current_user)
):
    """Get private messages between users (admin cannot see)"""
    # Get or create conversation
    conv = supabase.table("private_conversations")\
        .filter(f"or=(and(user1_id.eq.{current_user['id']},user2_id.eq.{user_id}),and(user1_id.eq.{user_id},user2_id.eq.{current_user['id']}))")\
        .execute()
    
    if not conv.data:
        # Create new conversation
        conv = supabase.table("private_conversations").insert({
            "user1_id": current_user['id'],
            "user2_id": user_id
        }).execute()
        conv_id = conv.data[0]['id']
    else:
        conv_id = conv.data[0]['id']
    
    # Get messages
    messages = supabase.table("private_messages")\
        .select("*")\
        .eq("conversation_id", conv_id)\
        .order("created_at", desc=True)\
        .limit(limit)\
        .execute()
    
    # Mark messages as read
    supabase.table("private_messages")\
        .update({"is_read": True, "read_at": datetime.now().isoformat()})\
        .eq("conversation_id", conv_id)\
        .eq("receiver_id", current_user['id'])\
        .execute()
    
    return messages.data[::-1]

@router.post("/messages/private", response_model=MessageResponse)
async def send_private_message(
    message: PrivateMessageCreate,
    current_user = Depends(get_current_user)
):
    """Send private message (admin cannot access)"""
    # Get or create conversation
    conv = supabase.table("private_conversations")\
        .filter(f"or=(and(user1_id.eq.{current_user['id']},user2_id.eq.{message.receiver_id}),and(user1_id.eq.{message.receiver_id},user2_id.eq.{current_user['id']}))")\
        .execute()
    
    if not conv.data:
        conv = supabase.table("private_conversations").insert({
            "user1_id": current_user['id'],
            "user2_id": message.receiver_id
        }).execute()
        conv_id = conv.data[0]['id']
    else:
        conv_id = conv.data[0]['id']
    
    message_data = {
        "conversation_id": conv_id,
        "sender_id": current_user['id'],
        "receiver_id": message.receiver_id,
        "message": message.message,
        "file_url": message.file_url,
        "file_type": message.file_type,
        "voice_note_url": message.voice_note_url,
        "voice_note_duration": message.voice_note_duration
    }
    
    result = supabase.table("private_messages").insert(message_data).execute()
    new_message = result.data[0]
    
    # Notify receiver via WebSocket
    await manager.send_personal_message(new_message, message.receiver_id)
    
    # Create notification
    supabase.table("notifications").insert({
        "user_id": message.receiver_id,
        "type": "private_message",
        "title": "New Message",
        "message": f"{current_user['full_name']} sent you a message",
        "data": {"conversation_id": conv_id}
    }).execute()
    
    return MessageResponse(message="Message sent", data=new_message)

@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        # Verify token and get user
        user = await verify_websocket(token)
        user_id = user['id']
        
        await manager.connect(websocket, user_id)
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get('type') == 'typing':
                await manager.broadcast_to_group({
                    'type': 'typing',
                    'user_id': user_id,
                    'user_name': user['full_name'],
                    'group_id': message_data.get('group_id')
                }, message_data.get('group_id'))
            
            elif message_data.get('type') == 'message':
                # Save to database
                msg = {
                    "group_id": message_data.get('group_id'),
                    "sender_id": user_id,
                    "message": message_data.get('message'),
                    "created_at": datetime.now().isoformat()
                }
                result = supabase.table("chat_messages").insert(msg).execute()
                msg['id'] = result.data[0]['id']
                msg['sender'] = {'full_name': user['full_name'], 'avatar_url': user.get('avatar_url')}
                
                # Broadcast to group
                await manager.broadcast_to_group(msg, message_data.get('group_id'))
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        logger.info(f"User {user_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
