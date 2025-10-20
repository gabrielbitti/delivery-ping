"""Address CRUD endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.commons import get_db
from app.models.customer import CustomerDTO
from app.models.address import Address, AddressDTO
from app.schemas.address import CreateAddress, AddressOut

router = APIRouter(tags=['Addresses'])


@router.post("/addresses", response_model=AddressOut,
             status_code=status.HTTP_201_CREATED)
def create_address(address: CreateAddress, db: Session = Depends(get_db)):
    """Create a new address."""
    customer = CustomerDTO(db).get_by_id(address.customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    db_address = Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return db_address


@router.get("/addresses", response_model=List[AddressOut])
def get_addresses(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db)):
    """Get all addresses with pagination."""
    return db.query(Address).offset(skip).limit(limit).all()


@router.get("/addresses/{address_id}", response_model=AddressOut)
def get_address(address_id: int, db: Session = Depends(get_db)):
    """Get an address by ID."""
    address = AddressDTO(db).get_by_id(address_id)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )
    return address


@router.put("/addresses/{address_id}", response_model=AddressOut)
def update_address(
        address_id: int,
        customer_update: CreateAddress,
        db: Session = Depends(get_db)
):
    """Update an address by ID."""
    address = AddressDTO(db).get_by_id(address_id)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )

    for field, value in customer_update.model_dump().items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)

    return address
