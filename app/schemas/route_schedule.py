"""RouteSchedule schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
