"""Route schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

"""Route"""


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


"""RoutePoint"""


class CreateRoutePoint(BaseModel):
    """Schema for creating a route point."""

    route_id: int
    address_id: int
    sequence_order: int
    estimated_time: str
    distance_to_next: float
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class RoutePoint(CreateRoutePoint):
    """Schema for the response."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


"""RouteSchedule"""


class CreateRouteSchedule(BaseModel):
    """Schema for creating a route schedule."""

    route_id: int
    status: str
    schedule_date: datetime
    finish_date: Optional[datetime]

    class Config:
        from_attributes = True


class RouteSchedule(CreateRouteSchedule):
    """Schema for the response."""

    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
