from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List, Optional
from uuid import UUID
import shutil
import os
from datetime import datetime

# Models and Schemas
from app.models.payment import Payment
from app.schemas.payment import Payment as PaymentSchema, PaymentCreate, PaymentUpdate
from app.models.user import User

# Auth Dependency
from app.api.v1.endpoints.users import get_current_user 

# Service
from app.services.payment_service import payment_service, PaymentService

# Beanie CRUD operations (or implement a service layer later)

router = APIRouter()

# Define upload directory (make sure it exists or create on startup)
UPLOAD_DIR = "uploads/proofs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# TODO: Implement multi-tenancy filtering (based on current_user.condominium_id)

def get_payment_service(): # Dependency factory
    return payment_service

@router.get("/", response_model=List[PaymentSchema])
async def read_payments(
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service),
    skip: int = 0,
    limit: int = 100
):
    """Retrieve payments for the current user (filtered by service)."""
    payments = await service.get_payments_for_user(user=current_user, skip=skip, limit=limit)
    return payments

# Endpoint to upload payment proof
@router.post("/upload", response_model=PaymentSchema)
async def upload_payment_proof(
    payment_id: UUID = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service)
):
    """Upload a payment proof image and link it via the service."""
    try:
        payment = await service.upload_proof(payment_id=payment_id, file=file, user=current_user)
        return payment
    except HTTPException as e:
        raise e # Re-raise HTTP exceptions from the service
    except Exception as e:
        # Log general error e
        raise HTTPException(status_code=500, detail="An error occurred during file upload.")

# Endpoint for admin to update payment status
@router.put("/{payment_id}/status", response_model=PaymentSchema)
async def update_payment_status(
    payment_id: UUID,
    status_update: PaymentUpdate,
    current_user: User = Depends(get_current_user),
    service: PaymentService = Depends(get_payment_service)
):
    """Update the status of a payment via the service (Admin only)."""
    try:
        payment = await service.update_payment_status(payment_id=payment_id, status_update=status_update, admin_user=current_user)
        return payment
    except HTTPException as e:
        raise e # Re-raise HTTP exceptions
    except Exception as e:
        # Log general error e
        raise HTTPException(status_code=500, detail="An error occurred while updating payment status.")

# Add endpoints for creating/deleting payments if needed (likely admin function)
