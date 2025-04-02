from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from datetime import datetime
from uuid import UUID

# Service
from app.services.calendar_service import calendar_service, CalendarService
from app.services.calendar_service import CalendarEventCreate, CalendarEventUpdate # Import schemas from service for now

# Models & Schemas
from app.models.calendar_event import CalendarEvent
from pydantic import BaseModel # Placeholder
from app.models.user import User

# Auth Dependency
from app.api.v1.endpoints.users import get_current_user

router = APIRouter()

# Placeholder Schema - TODO: Move to schemas/calendar.py
class CalendarEventSchema(BaseModel):
    event_id: UUID # Use UUID
    title: str
    event_date: datetime
    description: Optional[str] = None
    class Config:
        from_attributes = True

def get_calendar_service():
    return calendar_service

@router.get("/", response_model=List[CalendarEventSchema])
async def read_calendar_events(
    current_user: User = Depends(get_current_user),
    service: CalendarService = Depends(get_calendar_service),
    skip: int = 0,
    limit: int = 100
):
    """Retrieve calendar events via service."""
    events = await service.get_events(user=current_user, skip=skip, limit=limit)
    return events

@router.post("/", response_model=CalendarEventSchema, status_code=status.HTTP_201_CREATED)
async def create_calendar_event(
    event_in: CalendarEventCreate,
    current_user: User = Depends(get_current_user),
    service: CalendarService = Depends(get_calendar_service)
):
    """Create a new calendar event via service (Admin only)."""
    try:
        event = await service.create_event(event_in=event_in, user=current_user)
        return event
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log error e
        raise HTTPException(status_code=500, detail="Could not create event.")

@router.put("/{event_id}", response_model=CalendarEventSchema)
async def update_calendar_event(
    event_id: UUID,
    event_in: CalendarEventUpdate,
    current_user: User = Depends(get_current_user),
    service: CalendarService = Depends(get_calendar_service)
):
    """Update an event via service (Admin only)."""
    try:
        event = await service.update_event(event_id=event_id, event_in=event_in, user=current_user)
        return event
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log error e
        raise HTTPException(status_code=500, detail="Could not update event.")

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_calendar_event(
    event_id: UUID,
    current_user: User = Depends(get_current_user),
    service: CalendarService = Depends(get_calendar_service)
):
    """Delete an event via service (Admin only)."""
    try:
        await service.delete_event(event_id=event_id, user=current_user)
        return None # No content response
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log error e
        raise HTTPException(status_code=500, detail="Could not delete event.")
