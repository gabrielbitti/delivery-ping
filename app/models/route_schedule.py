"""Route model implementation."""

from enum import Enum

from sqlalchemy import (Integer, Column, ForeignKey, DateTime,
                        Enum as SQLEnum)

from .abstract import BaseModel


class RouteScheduleStatus(Enum):
    PLANNED = 'planned'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class RouteSchedule(BaseModel):
    __tablename__ = 'route_schedule'

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey('route.id'), nullable=False)
    status = Column(SQLEnum(RouteScheduleStatus, name='route_schedule_status'),
                    nullable=False,
                    default=RouteScheduleStatus.PLANNED)
    schedule_date = Column(DateTime(timezone=True))
    finish_date = Column(DateTime(timezone=True))
