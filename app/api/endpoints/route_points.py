"""Route CRUD endpoints."""

from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.commons import get_db
from app.models.address import AddressDTO
from app.models.route import RoutePoint, RouteDTO
from app.schemas.route_point import RoutePointOut, CreateRoutePoint

router = APIRouter(tags=['Route Points'])


@router.post("/route-points", response_model=RoutePointOut,
             status_code=status.HTTP_201_CREATED)
def create_route_point(route_point: CreateRoutePoint,
                       db: Session = Depends(get_db)):
    """Create a new route_point."""
    route = RouteDTO(db).get_by_id(route_point.route_id)
    if not route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )

    address = AddressDTO(db).get_by_id(route_point.address_id)
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Address not found"
        )

    db_route_point = RoutePoint(**route_point.model_dump())
    db.add(db_route_point)
    db.commit()
    db.refresh(db_route_point)

    return db_route_point


@router.get("/route-points", response_model=List[RoutePointOut])
def get_routes(skip: int = 0, limit: int = 10,
               db: Session = Depends(get_db)):
    """Get all routes with pagination."""
    routes = db.query(RoutePoint).order_by(RoutePoint.sequence_order).offset(
        skip).limit(limit).all()
    return routes
