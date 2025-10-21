"""Customer domain."""

from fastapi import status, HTTPException
from sqlalchemy.orm import Session

# from app.models.customer import CustomerDTO


class CustomerDomain:
    def __init__(self, data: dict, db: Session):
        self.data = data
        self.db = db

    def validate_creation(self):
        self.__validate_whatsapp_format()

        # todo: verify if user already exists by CPF, CNPJ, email
        # user_exists = CustomerDTO(self.db).user_exists(self.data)

        return True

    def __validate_whatsapp_format(self):
        if not self.data.get("has_whatsapp"):
            return True

        cellphone = self.data.get("cellphone")
        if len(cellphone) > 14 or len(cellphone) < 11:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid cellphone format"
            )

        return None
