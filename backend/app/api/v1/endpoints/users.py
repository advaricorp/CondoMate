from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from uuid import UUID
import logging

from app.schemas.user import User as UserSchema
from app.services.user_service import get_user_service, UserService
from app.models.user import User
from app.security.auth import decode_access_token

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token") # Point to your token endpoint

async def get_current_user(token: str = Depends(oauth2_scheme), service: UserService = Depends(get_user_service)) -> User:
    logger.info("Getting current user")
    logger.info(f"Token received: {token[:20]}...")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        logger.warning("Token decode failed")
        raise credentials_exception
    
    logger.info(f"Token payload: {payload}")
    
    user_id_str: Optional[str] = payload.get("sub")
    # We don't strictly need tenant_id here, as it's fetched with the user model below
    # tenant_id: Optional[str] = payload.get("tenant_id") 

    if user_id_str is None:
        logger.warning("No user_id in token payload")
        raise credentials_exception
    
    try:
        user_uuid = UUID(user_id_str)
        logger.info(f"Converted user_id to UUID: {user_uuid}")
    except ValueError:
        logger.warning(f"Invalid UUID format: {user_id_str}")
        raise credentials_exception # Invalid UUID format
        
    user = await service.get_user_by_id(user_uuid)
    if user is None:
        logger.warning(f"User not found: {user_uuid}")
        raise credentials_exception
    if not user.is_active:
        logger.warning(f"Inactive user: {user_uuid}")
        raise HTTPException(status_code=400, detail="Inactive user")
    logger.info(f"Successfully retrieved user: {user.email}")
    return user # The returned User object contains the tenant_id


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Fetches the data for the currently authenticated user."""
    logger.info(f"Returning user data for: {current_user.email}")
    return current_user

# Add other user management endpoints here (e.g., update profile)
