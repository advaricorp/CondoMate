from beanie import Document
from pydantic import Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class DocumentStorage(Document):
    document_id: UUID = Field(default_factory=uuid4)
    filename: str
    file_url: str # Path or URL to the stored document
    description: Optional[str] = None
    condominium_id: Optional[str] = None # For multi-tenancy
    uploaded_by: Optional[str] = None # Link to user ID or name
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)

    class Settings:
        name = "documents" 