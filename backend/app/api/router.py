from fastapi import APIRouter

from app.api.routes import health

# Every API endpoint lives under /api. Feature routers are defined in
# app/api/routes/ and included here, e.g.:
#     from app.api.routes import products
#     api_router.include_router(products.router)
api_router = APIRouter(prefix="/api")
api_router.include_router(health.router)
