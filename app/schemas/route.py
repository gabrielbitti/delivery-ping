"""Route schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

"""Route"""


class CreateRoute(BaseModel):
    """Schema for creating a route."""

    name: str
    is_active: bool = True

    # class Config:
    #     from_attributes = True


class Route(CreateRoute):
    """Schema for route response."""

    id: str
    created_at: datetime
    updated_at: datetime


"""RoutePoint"""


class CreateRoutePoint(BaseModel):
    """Schema for creating a route."""

    route_id: int
    address_id: int
    sequence_order: int
    estimated_time: str
    distance_to_next: float
    notes: Optional[str] = None

    # class Config:
    #     from_attributes = True


class RoutePoint(CreateRoutePoint):
    """Schema for route response."""

    id: int
    created_at: datetime
    updated_at: datetime


"""RouteSchedule"""


class CreateRouteSchedule(BaseModel):
    """Schema for creating a route."""

    route_id: int
    status: str
    schedule_date: datetime
    finish_date: Optional[str] = None

    # class Config:
    #     from_attributes = True


class RouteSchedule(CreateRouteSchedule):
    """Schema for route response."""

    id: int
    created_at: datetime
    updated_at: datetime
