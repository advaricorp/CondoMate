from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from beanie import Document
from datetime import datetime

class TenantBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    max_users: int = Field(default=10, description="Maximum number of users allowed in this tenant")
    features: List[str] = Field(default_factory=list, description="List of features enabled for this tenant")
    tenant_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    max_users: Optional[int] = None
    features: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)

class Tenant(Document):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    max_users: int = Field(default=10, description="Maximum number of users allowed in this tenant")
    features: List[str] = Field(default_factory=list, description="List of features enabled for this tenant")
    tenant_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    current_users: int = Field(default=0, description="Current number of users in this tenant")

    class Settings:
        name = "tenants" 