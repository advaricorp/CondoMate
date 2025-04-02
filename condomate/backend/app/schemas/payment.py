# Pydantic schemas for Payment model will go here
# Example:
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    amount: Optional[float] = None
    status: Optional[str] = "Pendiente" # e.g., Pendiente, En Revisión, Pagado
    due_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    user_id: Optional[str] = None # Link to the user who made the payment
    proof_url: Optional[str] = None # URL to the uploaded proof

class PaymentCreate(PaymentBase):
    amount: float
    user_id: str
    due_date: datetime

class PaymentUpdate(PaymentBase):
    status: Optional[str] = None
    payment_date: Optional[datetime] = None
    proof_url: Optional[str] = None

class PaymentInDBBase(PaymentBase):
    id: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Payment(PaymentInDBBase):
    pass
