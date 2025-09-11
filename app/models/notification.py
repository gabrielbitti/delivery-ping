"""Notification model implementation."""

from enum import Enum

from sqlalchemy import (String, Integer, Column, ForeignKey,
                        Enum as SQLEnum, DateTime)

from .abstract import BaseModel


class NotificationType(Enum):
    PRE_ROUTE = 'pre_route'
    CONFIRMATION = 'confirmation'


class NotificationStatus(Enum):
    PENDING = 'pending'
    SENT = 'sent'
    ERROR = 'error'


class Notification(BaseModel):
    __tablename__ = 'notification'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    route_schedule_id = Column(Integer, ForeignKey('route_schedule.id'), nullable=False) # route_id or route_schedule
    type = Column(SQLEnum(NotificationType, name='notification_type'),
                  nullable=False, default=NotificationType.PRE_ROUTE)
    status = Column(SQLEnum(NotificationStatus, name='notification_status'),
                    nullable=False, default=NotificationStatus.PENDING)
    scheduled_date = Column(String)
    sent_date = Column(DateTime(timezone=True))
    message = Column(String)
    customer_response = Column(String, nullable=True)
