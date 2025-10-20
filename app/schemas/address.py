"""Address schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateAddress(BaseModel):
    """Schema for creating a customer."""

    customer_id: int
    complete_address: str
    city: str
    state: str
    country: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_primary: bool = True

    class Config:
        from_attributes = True


class AddressOut(CreateAddress):
    """Schema for customer response."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
