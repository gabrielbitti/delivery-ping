"""Route model implementation."""

import enum

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    ForeignKey, Index, UniqueConstraint, CheckConstraint,
    Float, Text, Enum
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql import func

from .abstract import BaseModel


class RouteStatus(enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Route(BaseModel):
    __tablename__ = "route"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    points = relationship(
        "RoutePoint",
        back_populates="route",
        cascade="all, delete-orphan",
        order_by="RoutePoint.sequence_order"
    )
    schedules = relationship(
        "RouteSchedule",
        back_populates="route",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_route_active', 'is_active'),
    )


class RoutePoint(BaseModel):
    __tablename__ = "route_point"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(
        Integer,
        ForeignKey("route.id", ondelete="CASCADE"),
        nullable=False
    )
    address_id = Column(
        Integer,
        ForeignKey("address.id", ondelete="RESTRICT"),
        nullable=False
    )
    sequence_order = Column(Integer, nullable=False)
    estimated_time = Column(Integer)  # minutos no ponto
    distance_to_next = Column(Float)  # km até próximo ponto
    notes = Column(Text)

    route = relationship("Route", back_populates="points")
    address = relationship("Address", back_populates="route_points")

    __table_args__ = (
        UniqueConstraint('route_id', 'sequence_order',
                         name='uq_route_sequence'),
        UniqueConstraint('route_id', 'address_id', name='uq_route_address'),
        CheckConstraint('sequence_order > 0', name='positive_sequence'),
        Index('idx_route_point_composite', 'route_id', 'sequence_order'),
    )

    @validates('sequence_order')
    def validate_sequence(self, key, value):
        if value <= 0:
            raise ValueError("Sequência deve ser positiva")
        return value


class RouteSchedule(BaseModel):
    __tablename__ = "route_schedule"

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(
        Integer,
        ForeignKey("route.id", ondelete="CASCADE"),
        nullable=False
    )
    status = Column(
        Enum(RouteStatus),
        default=RouteStatus.PENDING,
        nullable=False,
        index=True
    )
    schedule_date = Column(DateTime(timezone=True), nullable=False, index=True)
    finish_date = Column(DateTime(timezone=True))

    route = relationship("Route", back_populates="schedules")
    notifications = relationship(
        "Notification",
        back_populates="schedule",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_schedule_date_status', 'schedule_date', 'status'),
        CheckConstraint(
            'finish_date IS NULL OR finish_date > schedule_date',
            name='valid_finish_date'
        ),
    )
