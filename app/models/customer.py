"""Customer model implementation."""

from sqlalchemy import String, Integer, Column, Boolean

from .abstract import BaseModel


class Customer(BaseModel):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    complete_name = Column(String, nullable=True)
    nickname = Column(String, nullable=True)
    cellphone = Column(String(20), nullable=True)
    has_whatsapp = Column(Boolean, nullable=True)
    cpf = Column(String, nullable=True)
    cnpj = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # address = Address
