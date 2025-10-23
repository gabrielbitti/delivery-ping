"""Route routes."""

from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.commons import get_db
from app.models.route import RouteDTO
from app.schemas.route import Route as RouteSchema, CreateRoute

router = APIRouter(tags=['Route Web Pages'])

templates = Jinja2Templates(directory="templates")


@router.post("/routes", response_model=RouteSchema,
             status_code=status.HTTP_201_CREATED)
def create_route(route: CreateRoute, db: Session = Depends(get_db)):
    """Create a new route."""
    return RouteDTO(db).insert(route)


@router.get("/routes/{route_id}", response_model=RouteSchema)
def get_route(route_id: int, db: Session = Depends(get_db)):
    """Get a route by ID."""
    route = RouteDTO(db).get_by_id(route_id)
    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found"
        )
    return route


@router.patch("/routes/{route_id}", response_model=RouteSchema)
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


@router.get("/web/routes", response_class=HTMLResponse)
def routes_page(request: Request, db: Session = Depends(get_db)):
    """Render the routes list page."""
    routes = RouteDTO(db).get_all()
    return templates.TemplateResponse(
        "routes/list.html",
        {"request": request, "routes": routes}
    )


@router.get("/web/routes/new", response_class=HTMLResponse)
def new_route_page(request: Request):
    """Render the new route form page."""
    return templates.TemplateResponse(
        "routes/form.html",
        {"request": request, "route": None, "action": "create"}
    )


@router.get("/web/routes/{route_id}", response_class=HTMLResponse)
def route_detail_page(request: Request, route_id: int,
                      db: Session = Depends(get_db)):
    """Render the route detail page."""
    route = RouteDTO(db).get_by_id(route_id)
    return templates.TemplateResponse(
        "routes/detail.html",
        {"request": request, "route": route}
    )


@router.get("/web/routes/{route_id}/edit", response_class=HTMLResponse)
def edit_route_page(request: Request, route_id: int,
                    db: Session = Depends(get_db)):
    """Render the edit route form page."""
    route = RouteDTO(db).get_by_id(route_id)
    return templates.TemplateResponse(
        "routes/form.html",
        {"request": request, "route": route, "action": "edit"}
    )
