"""Customer routes."""

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.commons import get_db
from app.domain.customer import CustomerDomain
from app.models.customer import CustomerDTO
from app.schemas.customer import Customer as CustomerSchema, CreateCustomer

router = APIRouter(tags=['Customer Web Pages'])
templates = Jinja2Templates(directory="templates")


@router.post("/customers", response_model=CustomerSchema,
             status_code=status.HTTP_201_CREATED)
def create_customer(customer: CreateCustomer, db: Session = Depends(get_db)):
    """Create a new customer."""
    CustomerDomain(customer.model_dump(), db).validate_before_creation()
    return CustomerDTO(db).insert(customer)


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


@router.get("/web/customers", response_class=HTMLResponse)
def customers_page(request: Request, db: Session = Depends(get_db)):
    """Render the customers list page."""
    customers = CustomerDTO(db).get_all()
    return templates.TemplateResponse(
        "customers/list.html",
        {"request": request, "customers": customers}
    )


@router.get("/web/customers/new", response_class=HTMLResponse)
def new_customer_page(request: Request):
    """Render the new customer form page."""
    return templates.TemplateResponse(
        "customers/form.html",
        {"request": request, "customer": None, "action": "create"}
    )


@router.get("/web/customers/{customer_id}", response_class=HTMLResponse)
def customer_detail_page(request: Request, customer_id: int,
                         db: Session = Depends(get_db)):
    """Render the customer detail page."""
    customer = CustomerDTO(db).get_by_id(customer_id)
    return templates.TemplateResponse(
        "customers/detail.html",
        {"request": request, "customer": customer}
    )


@router.get("/web/customers/{customer_id}/edit", response_class=HTMLResponse)
def edit_customer_page(request: Request, customer_id: int,
                       db: Session = Depends(get_db)):
    """Render the edit customer form page."""
    customer = CustomerDTO(db).get_by_id(customer_id)
    return templates.TemplateResponse(
        "customers/form.html",
        {"request": request, "customer": customer, "action": "edit"}
    )


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
