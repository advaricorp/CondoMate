from typing import List, Optional
from app.models.user import User, UserCreate, UserUpdate
from app.models.tenant import Tenant
from app.core.security import get_password_hash
from app.core.exceptions import TenantLimitExceeded, UserNotFound

class UserService:
    @staticmethod
    async def create_user(user: UserCreate) -> User:
        # Check tenant user limit
        tenant = await Tenant.get(user.tenant_id)
        if not tenant:
            raise ValueError("Invalid tenant")
        
        if tenant.current_users >= tenant.max_users:
            raise TenantLimitExceeded("Tenant user limit exceeded")
        
        # Create user with hashed password
        hashed_password = get_password_hash(user.password)
        db_user = User(
            **user.dict(exclude={'password'}),
            hashed_password=hashed_password
        )
        
        # Increment tenant user count
        tenant.current_users += 1
        await tenant.save()
        
        await db_user.save()
        return db_user

    @staticmethod
    async def get_user_by_id(user_id: str, tenant_id: str) -> Optional[User]:
        user = await User.get(user_id)
        if not user or user.tenant_id != tenant_id:
            raise UserNotFound("User not found")
        return user

    @staticmethod
    async def get_users_by_tenant(tenant_id: str) -> List[User]:
        return await User.find({"tenant_id": tenant_id}).to_list()

    @staticmethod
    async def update_user(user_id: str, tenant_id: str, user_update: UserUpdate) -> User:
        user = await UserService.get_user_by_id(user_id, tenant_id)
        
        update_data = user_update.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await user.save()
        return user

    @staticmethod
    async def delete_user(user_id: str, tenant_id: str) -> bool:
        user = await UserService.get_user_by_id(user_id, tenant_id)
        
        # Decrement tenant user count
        tenant = await Tenant.get(tenant_id)
        if tenant:
            tenant.current_users -= 1
            await tenant.save()
        
        await user.delete()
        return True 