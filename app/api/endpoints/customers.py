"""Customer CRUD endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.commons import get_db
from app.models.customer import Customer, CustomerDTO
from app.schemas.customer import Customer as CustomerSchema, CreateCustomer

router = APIRouter(prefix='/customers', tags=['Customers'])


@router.post("/", response_model=CustomerSchema,
             status_code=status.HTTP_201_CREATED)
def create_customer(customer: CreateCustomer, db: Session = Depends(get_db)):
    """Create a new customer."""
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


@router.get("/", response_model=List[CustomerSchema])
def get_customers(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db)):
    """Get all customers with pagination."""
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers


@router.get("/{customer_id}", response_model=CustomerSchema)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a customer by ID."""
    customer = CustomerDTO(db).get_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer


@router.put("/{customer_id}", response_model=CustomerSchema)
def update_customer(
        customer_id: int,
        customer_update: CreateCustomer,
        db: Session = Depends(get_db)
):
    """Update a customer by ID."""
    customer = CustomerDTO(db).get_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    for field, value in customer_update.model_dump().items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    return customer


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer by ID."""
    customer = CustomerDTO(db).get_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # todo: nao deletar, apenas atualizar campo "deleted_at"
    # customer = CustomerDTO(db).delete(customer_id)

    db.delete(customer)
    db.commit()
