"""RoutePoint schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateRoutePoint(BaseModel):
    """Schema for creating a route point."""

    route_id: int
    address_id: int
    sequence_order: int
    estimated_time: int
    distance_to_next: float
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class RoutePointOut(CreateRoutePoint):
    """Schema for the response."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
