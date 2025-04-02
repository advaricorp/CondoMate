from fastapi import Request, HTTPException
from typing import Optional
from app.core.config import settings
from app.models.tenant import Tenant
from app.models.user import User
from app.security.auth import verify_token
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of public paths that don't require tenant validation
public_paths = [
    "/api/v1/auth/token",
    "/api/v1/auth/register",
    "/api/v1/health"
]

async def get_tenant_from_token(request: Request) -> Optional[str]:
    """Extract tenant_id from the JWT token in the request header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("No valid Authorization header found")
        return None
    
    token = auth_header.split(" ")[1]
    logger.info(f"Extracted token: {token[:20]}...")
    
    payload = verify_token(token)
    if not payload:
        logger.warning("Token verification failed")
        return None
        
    logger.info(f"Token payload: {payload}")
    return payload.get("tenant_id")

async def tenant_middleware(request: Request, call_next):
    """Middleware to handle tenant-based access control."""
    logger.info(f"Processing request: {request.method} {request.url.path}")
    logger.info(f"Request headers: {dict(request.headers)}")
    
    # Skip tenant check for public paths
    if request.url.path in public_paths:
        logger.info(f"Skipping tenant check for public path: {request.url.path}")
        return await call_next(request)
    
    # Special handling for /users/me endpoint
    if request.url.path == "/api/v1/users/me":
        logger.info("Handling /users/me endpoint")
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.warning("No valid Authorization header for /users/me")
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        # Continue with the request
        response = await call_next(request)
        logger.info(f"/users/me response status: {response.status_code}")
        return response
    
    # For all other endpoints, proceed with normal flow
    response = await call_next(request)
    return response

def require_tenant_access():
    """Dependency to ensure tenant access is required."""
    async def tenant_access(request: Request):
        tenant_id = await get_tenant_from_token(request)
        if not tenant_id:
            raise HTTPException(status_code=401, detail="Tenant access required")
        return tenant_id
    return tenant_access 