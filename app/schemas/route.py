"""Route schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateRoute(BaseModel):
    """Schema for creating a route."""

    name: str
    is_active: bool = True

    class Config:
        from_attributes = True


class Route(CreateRoute):
    """Schema for route response."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
