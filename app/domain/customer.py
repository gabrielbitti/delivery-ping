"""Customer domain."""

from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from app.models.customer import CustomerDTO


class CustomerDomain:
    def __init__(self, data: dict, db: Session):
        self.data = data
        self.db = db

    def validate_before_creation(self):
        cellphone = self.data.get("cellphone")
        if cellphone and (len(cellphone) > 14 or len(cellphone) < 11):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid cellphone format"
            )

        customer_exists = CustomerDTO(self.db).user_exists(self.data)
        if customer_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer already exists"
            )

        return True
