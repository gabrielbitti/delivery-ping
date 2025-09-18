"""Customer model implementation."""

from sqlalchemy import String, Integer, Column, Boolean, Index
from sqlalchemy.orm import relationship

from .abstract import BaseModel


class Customer(BaseModel):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    complete_name = Column(String(255), nullable=False)
    nickname = Column(String(100))
    cellphone = Column(String(20), nullable=False)
    has_whatsapp = Column(Boolean, default=False)
    cpf = Column(String(11), unique=True, index=True)
    cnpj = Column(String(14), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    addresses = relationship(
        "Address",
        back_populates="customer",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    notifications = relationship(
        "Notification",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_customer_active_name', 'is_active', 'complete_name'),
        {'comment': 'Tabela de clientes do sistema'}
    )