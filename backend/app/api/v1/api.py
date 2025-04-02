from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, payments, calendar, documents, health, ai

api_router = APIRouter()

# Include routers from specific endpoint files
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["Calendar"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])

# Add more routers as needed
