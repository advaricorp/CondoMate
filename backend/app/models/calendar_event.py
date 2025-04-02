from beanie import Document
from pydantic import Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class CalendarEvent(Document):
    event_id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    event_date: datetime
    condominium_id: Optional[str] = None # For multi-tenancy
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)

    class Settings:
        name = "calendar_events" 