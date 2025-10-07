"""Route CRUD endpoints."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.commons import get_db
from app.models.route import Route, RouteDTO
from app.schemas.route import Route as RouteSchema, CreateRoute

router = APIRouter(prefix='/routes', tags=['Routes'])


@router.post("/", response_model=RouteSchema,
             status_code=status.HTTP_201_CREATED)
def create_route(route: CreateRoute, db: Session = Depends(get_db)):
    """Create a new route."""
    db_route = Route(**route.model_dump())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)

    return db_route


@router.get("/", response_model=List[RouteSchema])
def get_routes(skip: int = 0, limit: int = 10,
               db: Session = Depends(get_db)):
    """Get all routes with pagination."""
    routes = db.query(Route).offset(skip).limit(limit).all()
    return routes


@router.get("/{route_id}", response_model=RouteSchema)
def get_route(route_id: int, db: Session = Depends(get_db)):
    """Get a route by ID."""
    route = RouteDTO(db).get_by_id(route_id)
    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    return route


@router.patch("/{route_id}", response_model=RouteSchema)
def update_route(
        route_id: int,
        route_update: CreateRoute,
        db: Session = Depends(get_db)
):
    """Update a route by ID."""
    route = RouteDTO(db).get_by_id(route_id)
    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )

    for field, value in route_update.model_dump().items():
        setattr(route, field, value)

    db.commit()
    db.refresh(route)

    return route
