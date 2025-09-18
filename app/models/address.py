"""Address model implementation."""

from sqlalchemy import (
    Column, Integer, String, Float, Boolean,
    ForeignKey, DateTime, Index, CheckConstraint,
    text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .abstract import BaseModel


class Address(BaseModel):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    customer_id = Column(
        Integer,
        ForeignKey("customer.id", ondelete="CASCADE"),
        nullable=False
    )
    complete_address = Column(String(500), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    state = Column(String(50), nullable=False)
    country = Column(String(50), default="Brasil")
    zip_code = Column(String(10))
    latitude = Column(Float)
    longitude = Column(Float)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="addresses")
    route_points = relationship("RoutePoint", back_populates="address")

    __table_args__ = (
        Index('idx_address_city_customer', 'city', 'customer_id'),

        Index('idx_address_coordinates', 'latitude', 'longitude'),

        Index(
            'idx_one_primary_address',
            'customer_id',
            unique=True,
            postgresql_where=text('is_primary = true')
        ),

        CheckConstraint(
            'latitude >= -90 AND latitude <= 90',
            name='valid_latitude'
        ),
        CheckConstraint(
            'longitude >= -180 AND longitude <= 180',
            name='valid_longitude'
        ),
    )
