"""Customer schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateCustomer(BaseModel):
    """Schema for creating a customer."""

    complete_name: Optional[str] = None
    nickname: Optional[str] = None
    cellphone: Optional[str] = None
    has_whatsapp: Optional[bool] = None
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    email: Optional[str] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class Customer(CreateCustomer):
    """Schema for customer response."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
