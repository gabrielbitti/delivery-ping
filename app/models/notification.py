"""Notification model implementation."""

import enum

from sqlalchemy import (
    Column, Integer, DateTime, ForeignKey,
    Index, CheckConstraint, Enum, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .abstract import BaseModel


class NotificationType(enum.Enum):
    REMINDER = "reminder"
    CONFIRMATION = "confirmation"
    CANCELLATION = "cancellation"


class NotificationStatus(enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"


class Notification(BaseModel):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True)
    route_schedule_id = Column(
        Integer,
        ForeignKey("route_schedule.id", ondelete="CASCADE"),
        nullable=False
    )
    customer_id = Column(
        Integer,
        ForeignKey("customer.id", ondelete="CASCADE"),
        nullable=False
    )
    type = Column(
        Enum(NotificationType),
        default=NotificationType.REMINDER,
        nullable=False
    )
    status = Column(
        Enum(NotificationStatus),
        default=NotificationStatus.PENDING,
        nullable=False,
        index=True
    )
    scheduled_date = Column(DateTime(timezone=True), nullable=False,
                            index=True)
    sent_date = Column(DateTime(timezone=True))
    message = Column(Text, nullable=False)
    customer_response = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    schedule = relationship("RouteSchedule", back_populates="notifications")
    customer = relationship("Customer", back_populates="notifications")

    __table_args__ = (
        Index(
            'idx_notification_pending',
            'scheduled_date',
            'status',
            postgresql_where="status IN ('pending', 'failed')"
        ),

        CheckConstraint(
            "sent_date IS NULL OR sent_date >= scheduled_date",
            name='valid_sent_date'
        ),
    )
