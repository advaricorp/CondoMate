# Pydantic schemas for User model will go here
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    role: Optional[str] = "user"
    tenant_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    tenant_id: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Additional properties stored in DB
class UserInDB(UserBase):
    user_id: UUID
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

# Additional properties to return via API
class User(UserBase):
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
