"""
app_router.py

This file contains the main router for the entire application.
"""

# Import modules and libraries
from fastapi import APIRouter
import api.user_router as user_router
import api.login_router as login_router
import api.box_router as box_router
import api.extinguisher_router as extinguisher_router

app_router = APIRouter()
"""
The main router for the entire application.
"""

# Include the other routers
app_router.include_router(user_router.router, prefix="/users", tags=["users"])
app_router.include_router(login_router.router, tags=["login"])
app_router.include_router(box_router.router, prefix="/boxes", tags=["boxes"])
app_router.include_router(extinguisher_router.router, prefix="/extinguishers", tags=["extinguishers"])