"""API endpoints router initialization"""
from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.inspections import router as inspections_router
from app.api.verify import router as verify_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(inspections_router, tags=["Inspections"])
api_router.include_router(verify_router, tags=["Verification"])
