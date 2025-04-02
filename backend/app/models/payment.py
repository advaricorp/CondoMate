from beanie import Document, Link
from pydantic import Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

from app.models.user import User # Import User for linking

class Payment(Document):
    payment_id: UUID = Field(default_factory=uuid4)
    user: Link[User]
    amount: float
    status: str = "Pendiente" # Pendiente, En Revisión, Pagado
    due_date: datetime
    payment_date: Optional[datetime] = None
    proof_url: Optional[str] = None
    condominium_id: Optional[str] = None # For multi-tenancy
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(from_attributes=True)

    class Settings:
        name = "payments"
