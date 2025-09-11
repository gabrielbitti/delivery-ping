"""RouteCity model implementation."""

from sqlalchemy import Integer, Column, ForeignKey

from .abstract import BaseModel


class RouteCustomer(BaseModel):
    __tablename__ = 'route_customer'

    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey('route.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)

    # customer =
    # route =
