from typing import List, Optional
from uuid import UUID
import shutil
import os

from fastapi import UploadFile, HTTPException

from app.models.document_storage import DocumentStorage
from app.models.user import User
from pydantic import BaseModel

UPLOAD_DIR_DOCS = "uploads/documents"
os.makedirs(UPLOAD_DIR_DOCS, exist_ok=True)

# Placeholder schemas
class DocumentCreate(BaseModel):
    description: Optional[str] = None

class DocumentUpdate(BaseModel):
    description: Optional[str] = None

class DocumentService:
    async def get_documents(self, user: User, skip: int = 0, limit: int = 100) -> List[DocumentStorage]:
        query = DocumentStorage.find_all()
        if user.condominium_id:
            query = query.find(DocumentStorage.condominium_id == user.condominium_id)
        else:
            # Define logic for non-condo users
            pass # Currently allows seeing all non-condo docs

        docs = await query.sort(-DocumentStorage.created_at).skip(skip).limit(limit).to_list()
        return docs

    async def upload_document(self, file: UploadFile, user: User, description: Optional[str] = None) -> DocumentStorage:
        if not user.is_superuser: # Only admins can upload docs
            raise HTTPException(status_code=403, detail="Permission denied")

        allowed_types = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Invalid file type.")

        filename = file.filename
        file_path = os.path.join(UPLOAD_DIR_DOCS, filename)
        
        # Handle potential overwrite
        if os.path.exists(file_path):
            file_extension = os.path.splitext(filename)[1]
            base_name = os.path.splitext(filename)[0]
            unique_id = str(UUID())[:8] # Short unique ID
            filename = f"{base_name}_{unique_id}{file_extension}"
            file_path = os.path.join(UPLOAD_DIR_DOCS, filename)

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            # Log error e
            raise HTTPException(status_code=500, detail="Could not save document file.")
        finally:
            file.file.close()

        doc_record = DocumentStorage(
            filename=filename,
            file_url=f"/{UPLOAD_DIR_DOCS}/{filename}",
            description=description,
            uploaded_by=user.email,
            condominium_id=user.condominium_id # Assign admin's condo ID
        )
        await doc_record.insert()
        return doc_record

    async def delete_document(self, document_id: UUID, user: User) -> None:
        if not user.is_superuser:
            raise HTTPException(status_code=403, detail="Permission denied")

        doc = await DocumentStorage.find_one(DocumentStorage.document_id == document_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        # Ensure admin is deleting doc in their own condo
        if user.condominium_id and doc.condominium_id != user.condominium_id:
            raise HTTPException(status_code=403, detail="Cannot delete document in another condominium")

        # Delete the file from storage
        try:
            file_path = os.path.join(UPLOAD_DIR_DOCS, doc.filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            # Log error e - but proceed to delete DB record
            print(f"Warning: Could not delete document file {doc.filename}: {e}")
            
        await doc.delete()
        return None

# Create service instance
document_service = DocumentService() 