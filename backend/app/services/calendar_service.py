from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import HTTPException

from app.models.calendar_event import CalendarEvent
from app.models.user import User
# Import schemas when defined
# from app.schemas.calendar import CalendarEventCreate, CalendarEventUpdate 
from pydantic import BaseModel # Placeholder

# Placeholder schemas
class CalendarEventCreate(BaseModel):
    title: str
    event_date: datetime
    description: Optional[str] = None

class CalendarEventUpdate(BaseModel):
    title: Optional[str] = None
    event_date: Optional[datetime] = None
    description: Optional[str] = None

class CalendarService:
    async def get_events(self, user: User, skip: int = 0, limit: int = 100) -> List[CalendarEvent]:
        query = CalendarEvent.find_all()
        if user.condominium_id:
            query = query.find(CalendarEvent.condominium_id == user.condominium_id)
        else:
            # Or maybe non-condo users can't see any events? Define this logic.
            pass # Currently allows non-condo users to see all (if no condo_id set on event)

        events = await query.sort(+CalendarEvent.event_date).skip(skip).limit(limit).to_list()
        return events

    async def create_event(self, event_in: CalendarEventCreate, user: User) -> CalendarEvent:
        if not user.is_superuser: # Only admins can create events
            raise HTTPException(status_code=403, detail="Permission denied")

        event = CalendarEvent(
            title=event_in.title,
            description=event_in.description,
            event_date=event_in.event_date,
            condominium_id=user.condominium_id # Assign admin's condo ID
        )
        await event.insert()
        return event

    async def update_event(self, event_id: UUID, event_in: CalendarEventUpdate, user: User) -> CalendarEvent:
        if not user.is_superuser:
            raise HTTPException(status_code=403, detail="Permission denied")

        event = await CalendarEvent.find_one(CalendarEvent.event_id == event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        # Ensure admin is updating event in their own condo
        if user.condominium_id and event.condominium_id != user.condominium_id:
            raise HTTPException(status_code=403, detail="Cannot update event in another condominium")

        update_data = event_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)

        await event.save()
        return event

    async def delete_event(self, event_id: UUID, user: User) -> None:
        if not user.is_superuser:
            raise HTTPException(status_code=403, detail="Permission denied")

        event = await CalendarEvent.find_one(CalendarEvent.event_id == event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Ensure admin is deleting event in their own condo
        if user.condominium_id and event.condominium_id != user.condominium_id:
            raise HTTPException(status_code=403, detail="Cannot delete event in another condominium")
            
        await event.delete()
        return None

# Instance
calendar_service = CalendarService() 