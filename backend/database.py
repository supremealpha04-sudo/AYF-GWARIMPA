import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

url: str = os.getenv("SUPABASE_URL", "")
key: str = os.getenv("SUPABASE_KEY", "")
service_key: str = os.getenv("SUPABASE_SERVICE_KEY", "")

if not url or not key:
    logger.error("SUPABASE_URL and SUPABASE_KEY must be set in environment")
    raise ValueError("Missing Supabase credentials")

supabase: Client = create_client(url, key)
supabase_admin: Client = create_client(url, service_key) if service_key else supabase

def get_user_by_email(email: str):
    """Get user by email"""
    try:
        result = supabase.table("users").select("*").eq("email", email).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        return None

def get_user_by_id(user_id: str):
    """Get user by ID"""
    try:
        result = supabase.table("users").select("*").eq("id", user_id).execute()
        return result.data[0] if result.data else None
    except Exception as e:
        logger.error(f"Error fetching user: {str(e)}")
        return None

def update_user_last_seen(user_id: str):
    """Update user's last seen timestamp"""
    try:
        supabase.table("users").update({"last_seen": "now()"}).eq("id", user_id).execute()
    except Exception as e:
        logger.error(f"Error updating last_seen: {str(e)}")
