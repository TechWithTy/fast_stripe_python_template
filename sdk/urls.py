from fastapi import APIRouter

from .views import router as stripe_router

# This file sets up the FastAPI router for Stripe integration endpoints.
# All endpoints are now defined in views.py using FastAPI's APIRouter.

router = APIRouter()
router.include_router(stripe_router, prefix="/stripe", tags=["stripe"])
