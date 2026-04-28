from fastapi import APIRouter, HTTPException, Depends, Query
from datetime import date, datetime, timedelta
from typing import List, Optional
from ..database import supabase
from ..models import YearlyEventCreate, YearlyEventUpdate, MessageResponse
from ..middleware.auth import get_current_user, require_role
from dateutil.rrule import rrule, WEEKLY, MONTHLY, YEARLY
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.post("/events", response_model=MessageResponse)
async def create_event(
    event: YearlyEventCreate,
    current_user = Depends(require_role(["admin", "gen_president", "gen_sec"]))
):
    """Create yearly plan events (Admin only)"""
    events_to_insert = []
    
    # Handle recurring events
    if event.is_recurring and event.recurrence_pattern:
        recurrence_map = {
            'weekly': WEEKLY,
            'monthly': MONTHLY,
            'yearly': YEARLY
        }
        
        pattern = recurrence_map.get(event.recurrence_pattern)
        if pattern:
            end_date = event.recurrence_end_date or date(event.event_date.year + 1, 12, 31)
            dates = list(rrule(pattern, dtstart=event.event_date, until=end_date))
            
            for dt in dates:
                events_to_insert.append({
                    "title": event.title,
                    "description": event.description,
                    "event_date": dt.date().isoformat(),
                    "event_level": event.event_level,
                    "parish_id": event.parish_id if event.event_level == 'parish' else None,
                    "is_recurring": True,
                    "recurrence_pattern": event.recurrence_pattern,
                    "recurrence_end_date": end_date.isoformat(),
                    "created_by": current_user['id']
                })
    else:
        events_to_insert.append({
            "title": event.title,
            "description": event.description,
            "event_date": event.event_date.isoformat(),
            "event_level": event.event_level,
            "parish_id": event.parish_id if event.event_level == 'parish' else None,
            "is_recurring": False,
            "created_by": current_user['id']
        })
    
    # Insert events
    for evt in events_to_insert:
        result = supabase.table("yearly_events").insert(evt).execute()
        
        # Send notifications
        await trigger_event_notifications(result.data[0] if result.data else evt)
    
    return MessageResponse(
        message=f"Created {len(events_to_insert)} events",
        data={"count": len(events_to_insert)}
    )

@router.get("/events")
async def get_calendar_events(
    month: int = Query(..., ge=1, le=12),
    year: int = Query(..., ge=2024, le=2030),
    current_user = Depends(get_current_user)
):
    """Get events for a specific month"""
    start_date = date(year, month, 1)
    if month == 12:
        end_date = date(year, 12, 31)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    
    # Build query based on user role and parish
    query = supabase.table("yearly_events")\
        .select("*")\
        .gte("event_date", start_date.isoformat())\
        .lte("event_date", end_date.isoformat())
    
    # Filter based on user's parish and event level
    if current_user['role'] == 'member':
        # Members see archdeaconry, diocese, and their own parish events
        query = query.filter(
            f"or=(event_level.eq.archdeaconry,event_level.eq.diocese,and(event_level.eq.parish,parish_id.eq.{current_user['parish_id']}))"
        )
    
    result = query.order("event_date").execute()
    
    # Add display text for diocese
    events = []
    for event in result.data:
        if event['event_level'] == 'diocese':
            event['display_text'] = "DIOCESE: " + event['title']
        else:
            event['display_text'] = event['title']
        events.append(event)
    
    return events

@router.put("/events/{event_id}", response_model=MessageResponse)
async def update_event(
    event_id: str,
    event_update: YearlyEventUpdate,
    current_user = Depends(require_role(["admin", "gen_president", "gen_sec"]))
):
    """Update an event"""
    update_data = event_update.dict(exclude_unset=True)
    if update_data:
        supabase.table("yearly_events").update(update_data).eq("id", event_id).execute()
    return MessageResponse(message="Event updated successfully")

@router.delete("/events/{event_id}", response_model=MessageResponse)
async def delete_event(
    event_id: str,
    current_user = Depends(require_role(["admin"]))
):
    """Delete an event (Admin only)"""
    supabase.table("yearly_events").delete().eq("id", event_id).execute()
    return MessageResponse(message="Event deleted successfully")

async def trigger_event_notifications(event):
    """Send notifications for new events"""
    # Get all active users
    users = supabase.table("users").select("id").eq("is_active", True).execute()
    
    for user in users.data:
        # Check if user should receive this notification
        if event.get('event_level') == 'parish' and event.get('parish_id'):
            user_parish = supabase.table("users").select("parish_id").eq("id", user['id']).single().execute()
            if user_parish.data and user_parish.data['parish_id'] != event['parish_id']:
                continue
        
        # Create notification
        supabase.table("notifications").insert({
            "user_id": user['id'],
            "type": "event",
            "title": "New Event Added",
            "message": f"{event['title']} on {event['event_date']}",
            "data": {"event_id": event.get('id')}
        }).execute()
