"""Route model implementation."""

from sqlalchemy import String, Integer, Column, Boolean

from .abstract import BaseModel


class Route(BaseModel):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_active = Column(Boolean, nullable=False, default=True)

    # route_customers = [] # todo
    # route_schedules = [] # todo
