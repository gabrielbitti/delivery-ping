"""Customer model implementation."""

from sqlalchemy import String, Integer, Column, Boolean, Index, text

from .abstract import BaseModel
from ..schemas.customer import CreateCustomer


# from sqlalchemy.orm import relationship, validates


class Customer(BaseModel):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    complete_name = Column(String(255), nullable=False)
    nickname = Column(String(100))
    cellphone = Column(String(20), nullable=False)
    has_whatsapp = Column(Boolean, default=False)
    cpf = Column(String(11), unique=True, index=True)
    cnpj = Column(String(18), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # addresses = relationship(
    #     "Address",
    #     back_populates="customer",
    #     cascade="all, delete-orphan",
    #     lazy="selectin"
    # )
    # notifications = relationship(
    #     "Notification",
    #     back_populates="customer",
    #     cascade="all, delete-orphan"
    # )

    __table_args__ = (
        Index('idx_customer_active_name', 'is_active', 'complete_name'),
        {'comment': 'Tabela de clientes do sistema'}
    )

    # @validates('cellphone')
    # def validate_cellphone(self, key, value):
    #     if len(value) > 14:  # ex: '5527998393682':
    #         raise ValueError("Formato deve ser: 55987654321")
    #     return value
    #
    # @validates('cpf')
    # def validate_cpf(self, key, value):
    #     if len(value) != 11:
    #         raise ValueError("Formato deve ser: 12345678901")
    #     return value
    #
    # @validates('cnpj')
    # def validate_cnpj(self, key, value):
    #     if len(value) != 14:
    #         raise ValueError("Formato deve ser: 01227601200139")
    #     return value


class CustomerDTO:
    def __init__(self, db):
        self.db = db

    def get_all(self) -> list[Customer]:
        """Get all Customers."""
        return self.db.query(Customer).all()

    def get_by_id(self, pk: int) -> Customer:
        """Get a Customer by id."""
        return self.db.query(Customer).where(Customer.id == pk).first()

    def insert(self, customer: CreateCustomer) -> Customer:
        """Insert a Customer."""
        new_customer = Customer(**customer.model_dump())
        self.db.add(new_customer)
        self.db.commit()
        self.db.refresh(new_customer)

        return new_customer

    def user_exists(self, data: dict):
        """Check if a Customer exists by email, CPF or CNPJ."""
        conditions = []
        
        if data.get("email"):
            conditions.append(f"email = '{data.get('email')}'")
        if data.get("cpf"):
            conditions.append(f"cpf = '{data.get('cpf')}'")
        if data.get("cnpj"):
            conditions.append(f"cnpj = '{data.get('cnpj')}'")
        
        if not conditions:
            return False
            
        where_clause = " OR ".join(conditions)
        query = self.db.query(Customer).where(text(where_clause))
        
        return query.first()
