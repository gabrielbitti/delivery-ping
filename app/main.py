"""Main implementation."""

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.endpoints.addresses import router as addresses_router
from app.api.endpoints.customers import router as customers_router
from app.api.endpoints.route_points import router as router_points_router
from app.api.endpoints.routes import router as routes_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(addresses_router)
app.include_router(customers_router)
app.include_router(router_points_router)
app.include_router(routes_router)

# todo: configure CORS

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8007, reload=True)
