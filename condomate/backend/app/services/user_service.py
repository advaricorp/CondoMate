from typing import Optional
from uuid import UUID

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.security.auth import get_password_hash, verify_password

class UserService:
    async def get_user_by_email(self, email: str) -> Optional[User]:
        return await User.find_one(User.email == email)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        try:
            # Convert string to UUID if needed
            if isinstance(user_id, str):
                user_id = UUID(user_id)
            return await User.find_one(User.user_id == user_id)
        except ValueError:
            return None

    async def create_user(self, user_in: UserCreate) -> User:
        # Check if user already exists
        existing_user = await self.get_user_by_email(user_in.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        hashed_password = get_password_hash(user_in.password)
        user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            tenant_id=user_in.tenant_id,
            role=user_in.role,
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser
        )
        await user.insert()
        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.get_user_by_email(email)
        if not user or not user.is_active:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def update_user(self, user: User, user_in: UserUpdate) -> User:
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            user.hashed_password = hashed_password
            del update_data["password"]
        
        for field, value in update_data.items():
            setattr(user, field, value)
            
        await user.save()
        return user

    # Add methods for deleting users, managing roles/condos, etc. as needed

# Create a singleton instance
user_service = UserService()

# Dependency injection function
def get_user_service() -> UserService:
    return user_service
