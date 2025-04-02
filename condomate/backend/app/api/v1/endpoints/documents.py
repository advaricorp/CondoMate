from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from typing import List, Optional
from uuid import UUID

# Service
from app.services.document_service import document_service, DocumentService
from app.services.document_service import DocumentCreate # Import schema from service for now

# Models & Schemas
from app.models.document_storage import DocumentStorage
from pydantic import BaseModel # Placeholder
from app.models.user import User

# Auth Dependency
from app.api.v1.endpoints.users import get_current_user

router = APIRouter()

# Placeholder Schema - TODO: Move to schemas/document.py
class DocumentSchema(BaseModel):
    document_id: UUID # Use UUID
    filename: str
    file_url: str
    description: Optional[str] = None
    class Config:
         from_attributes = True

def get_document_service():
    return document_service

@router.get("/", response_model=List[DocumentSchema])
async def read_documents(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """Get documents for the current user's tenant."""
    # TODO: Implement document service and pagination
    return []

@router.post("/upload", response_model=DocumentSchema, status_code=status.HTTP_201_CREATED)
async def upload_document(
    description: Optional[str] = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    """Upload a document via service (Admin only)."""
    try:
        doc_record = await service.upload_document(file=file, user=current_user, description=description)
        return doc_record
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log error e
        raise HTTPException(status_code=500, detail="Could not upload document.")

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service)
):
    """Delete a document via service (Admin only)."""
    try:
        await service.delete_document(document_id=document_id, user=current_user)
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        # Log error e
        raise HTTPException(status_code=500, detail="Could not delete document.")
