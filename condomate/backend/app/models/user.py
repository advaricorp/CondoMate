from beanie import Document, Indexed
from pydantic import Field, EmailStr, BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    is_superuser: bool = False
    role: str = Field(default="user", description="User role within the tenant (admin, manager, user)")
    tenant_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None
    tenant_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    email: Indexed(EmailStr, unique=True)
    hashed_password: str
    full_name: str
    is_active: bool = True
    is_superuser: bool = False
    role: str = Field(default="user", description="User role within the tenant (admin, manager, user)")
    tenant_id: Indexed(str)  # Index tenant_id for faster lookups
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    class Settings:
        name = "users"
        indexes = [
            [("email", 1), ("tenant_id", 1)],  # Compound index for email + tenant_id
        ]

class UserWithTenant(BaseModel):
    user_id: UUID
    email: EmailStr
    full_name: str
    role: str
    tenant_id: str
    tenant_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
