"""Customer schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateCustomer(BaseModel):
    """Schema for creating a customer."""

    complete_name: str
    cellphone: str
    has_whatsapp: bool
    email: str
    address: str
    city: str
    state: str
    country: str
    zip_code: str
    latitude: str
    longitude: str
    is_active: bool = True

    class Config:
        from_attributes = True


class Customer(BaseModel):
    """Schema for customer response."""

    id: int
    complete_name: str
    cellphone: str
    has_whatsapp: bool
    email: Optional[str] = None
    address: str
    city: str
    state: str
    country: str
    zip_code: str
    latitude: str
    longitude: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
