from typing import List, Optional
from uuid import UUID
import shutil
import os
from datetime import datetime

from fastapi import UploadFile, HTTPException

from app.models.payment import Payment
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentUpdate

UPLOAD_DIR = "uploads/proofs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class PaymentService:

    async def get_payments_for_user(self, user: User, skip: int = 0, limit: int = 100) -> List[Payment]:
        # Basic implementation - requires multi-tenancy filter
        query = Payment.find(Payment.user.id == user.id)
        if user.condominium_id:  # Apply multi-tenancy filter if user has one
            query = query.find(Payment.condominium_id == user.condominium_id)
        
        payments = await query.sort(-Payment.created_at).skip(skip).limit(limit).to_list()
        return payments

    async def get_payment_by_id(self, payment_id: UUID, user: Optional[User] = None) -> Optional[Payment]:
        # If user is provided, ensure the payment belongs to them (or their condo)
        query = Payment.find(Payment.payment_id == payment_id)
        if user:
            # Check ownership OR if user is admin (admins might see all in their condo)
            is_owner = (Payment.user.id == user.id)
            # Basic multi-tenancy check (improve with roles)
            in_condo = (Payment.condominium_id == user.condominium_id)
            if user.is_superuser:  # Superuser can see any payment
                pass
            elif user.condominium_id:  # Regular user/admin checks ownership/condo
                # Logic might depend if non-admin users can see payments they didn't create
                # Assuming users only see their own, admins see their condo's
                if not is_owner and not (user.is_superuser and in_condo):  # Adjust admin logic as needed
                    return None  # Not authorized or not found for user/condo
                query = query.find(in_condo)
            else:  # User without condo_id can only see their own
                query = query.find(is_owner)
        
        payment = await query.first_or_none()
        return payment

    async def create_payment(self, payment_in: PaymentCreate, user: User) -> Payment:
        # Admins typically create payment obligations
        if not user.is_superuser:  # Adjust role check as needed
            raise HTTPException(status_code=403, detail="Permission denied")

        # Find the target user for whom the payment is being created
        target_user = await User.find_one(User.user_id == payment_in.user_id)  # Assuming user_id is passed in schema
        if not target_user:
            raise HTTPException(status_code=404, detail="Target user not found")
        
        # Ensure target user is in the same condo as the admin (if applicable)
        if user.condominium_id and target_user.condominium_id != user.condominium_id:
            raise HTTPException(status_code=403, detail="Cannot create payment for user in another condominium")

        payment = Payment(
            user=target_user,  # Link to the target user
            amount=payment_in.amount,
            due_date=payment_in.due_date,
            status="Pendiente",
            condominium_id=target_user.condominium_id  # Assign condo ID from target user
        )
        await payment.insert()
        return payment

    async def upload_proof(self, payment_id: UUID, file: UploadFile, user: User) -> Payment:
        payment = await self.get_payment_by_id(payment_id, user=user)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found or access denied")
        
        # Ensure the payment actually belongs to the user uploading the proof
        if payment.user.id != user.id:
            raise HTTPException(status_code=403, detail="Cannot upload proof for another user's payment")

        if payment.status == "Pagado":
            raise HTTPException(status_code=400, detail="Payment already marked as paid")

        if not file.content_type.startswith("image/"):  # Basic validation
            raise HTTPException(status_code=400, detail="Invalid file type, only images allowed.")

        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{payment_id}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            # Log error e
            raise HTTPException(status_code=500, detail="Could not save file.")
        finally:
            file.file.close()

        # TODO: Trigger OCR service
        # from .ocr_service import ocr_service
        # await ocr_service.process_proof(payment)
        
        return payment

    async def update_payment_status(self, payment_id: UUID, status_update: PaymentUpdate, admin_user: User) -> Payment:
        if not admin_user.is_superuser:  # Check if user is admin
            raise HTTPException(status_code=403, detail="Operation not permitted")

        # Admin should only update payments within their condominium (if applicable)
        payment = await self.get_payment_by_id(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Multi-tenancy check for admins
        if admin_user.condominium_id and payment.condominium_id != admin_user.condominium_id:
            raise HTTPException(status_code=403, detail="Cannot update payment in another condominium")

        # Update payment status
        payment.status = status_update.status
        payment.updated_at = datetime.utcnow()
        await payment.save()
        return payment

# Instance for dependency injection
payment_service = PaymentService()
