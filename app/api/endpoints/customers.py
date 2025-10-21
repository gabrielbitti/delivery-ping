"""Customer CRUD endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.commons import get_db
from app.domain.customer import CustomerDomain
from app.models.customer import Customer, CustomerDTO
from app.schemas.customer import Customer as CustomerSchema, CreateCustomer

router = APIRouter(tags=['Customers'])


@router.post("/customers", response_model=CustomerSchema,
             status_code=status.HTTP_201_CREATED)
def create_customer(customer: CreateCustomer, db: Session = Depends(get_db)):
    """Create a new customer."""
    CustomerDomain(customer.model_dump(), db).validate_before_creation()
    return CustomerDTO(db).insert(customer)


@router.get("/customers", response_model=List[CustomerSchema])
def get_customers(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db)):
    """Get all customers with pagination."""
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers


@router.get("/customers/{customer_id}", response_model=CustomerSchema)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a customer by ID."""
    customer = CustomerDTO(db).get_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer


@router.put("/customers/{customer_id}", response_model=CustomerSchema)
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
