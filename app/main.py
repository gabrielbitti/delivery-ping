"""Main implementation."""

import uvicorn
from fastapi import FastAPI

from app.api.endpoints.addresses import router as addresses_router
from app.api.endpoints.customers import router as customers_router
from app.api.endpoints.route_points import router as router_points_router
from app.api.endpoints.routes import router as router_router

prefix = '/api/v1'

app = FastAPI()
app.include_router(addresses_router, prefix=prefix)
app.include_router(customers_router, prefix=prefix)
app.include_router(router_points_router, prefix=prefix)
app.include_router(router_router, prefix=prefix)

# todo: configure CORS

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8007, reload=True)
