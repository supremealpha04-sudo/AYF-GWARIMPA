import os
from supabase import create_client
from typing import BinaryIO
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def upload_file(file: BinaryIO, path: str) -> str:
    """Upload file to Supabase Storage"""
    try:
        file_extension = file.filename.split('.')[-1] if file.filename else 'jpg'
        file_name = f"{uuid.uuid4()}.{file_extension}"
        full_path = f"{path}/{file_name}"
        
        # Read file content
        content = await file.read()
        
        # Upload to storage
        supabase.storage.from_("ayf-files").upload(full_path, content)
        
        # Get public URL
        public_url = supabase.storage.from_("ayf-files").get_public_url(full_path)
        
        return public_url
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        raise

async def delete_file(file_url: str):
    """Delete file from storage"""
    try:
        # Extract path from URL
        path = file_url.split("/")[-2:]
        path = "/".join(path)
        supabase.storage.from_("ayf-files").remove([path])
    except Exception as e:
        logger.error(f"File delete error: {str(e)}")
