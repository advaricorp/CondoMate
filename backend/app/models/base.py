from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class TenantBase(BaseModel):
    tenant_id: str = Field(..., description="The ID of the tenant this record belongs to")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True) 