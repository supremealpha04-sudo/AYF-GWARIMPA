from supabase import create_client
import os
import json
import asyncio
import logging

logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class RealtimeSubscriber:
    def __init__(self):
        self.subscriptions = {}
    
    def subscribe_to_channel(self, channel_name: str, callback):
        """Subscribe to a realtime channel"""
        channel = supabase.channel(channel_name)
        
        def handle_event(payload):
            callback(payload)
        
        channel.on("*", callback=handle_event)
        channel.subscribe()
        
        self.subscriptions[channel_name] = channel
        return channel
    
    def unsubscribe(self, channel_name: str):
        """Unsubscribe from channel"""
        if channel_name in self.subscriptions:
            self.subscriptions[channel_name].unsubscribe()
            del self.subscriptions[channel_name]

realtime = RealtimeSubscriber()
