from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Dict, Any
from app.core.db import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter()

@router.get("/", response_model=Dict[str, Any])
async def health_check(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Health check endpoint that verifies database connectivity and service status."""
    try:
        # Check database connectivity
        await db.command("ping")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "services": {
            "database": db_status,
            "api": "healthy"
        },
        "version": "1.0.0"
    } 