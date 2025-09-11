"""Address model implementation."""

from sqlalchemy import String, Integer, Column, ForeignKey

from .abstract import BaseModel


class Address(BaseModel):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    complete_address = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    country = Column(String, nullable=False, default='Brasil')
    zip_code = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)

    # customer = Customer