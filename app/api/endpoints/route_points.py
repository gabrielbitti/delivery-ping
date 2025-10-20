"""Route CRUD endpoints."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.commons import get_db
from app.models.route import RoutePoint
from app.schemas.route_point import RoutePointOut, CreateRoutePoint

router = APIRouter(tags=['Route Points'])


@router.post("/route-points", response_model=RoutePointOut,
             status_code=status.HTTP_201_CREATED)
def create_route_point(route_point: CreateRoutePoint,
                       db: Session = Depends(get_db)):
    """Create a new route_point."""
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
