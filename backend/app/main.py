#!/usr/bin/env python3
# main.py
"""
main.py
This module implements a FastAPI server for the demo application.
"""

# Import modules and libraries
import uvicorn
from fastapi import FastAPI
from config import APP_HOST, APP_PORT, APP_TITLE, APP_VERSION, APP_DESCRIPTION
from utils import init_database, init_test_database_data
from api.app_router import app_router

# Create a new instance of a FastAPI application named app
app = FastAPI(title=APP_TITLE, version=APP_VERSION, description=APP_DESCRIPTION)
app.include_router(app_router)

@app.on_event("startup")
def startup():
    # Create the initial database
    init_database()

    # Populate the database with test data when debugging
    init_test_database_data()

@app.get("/")
async def root():
    """
    Returns a welcome message.
    """
    return {"Message": "Welcome to the Fire Extinguisher Management System!"}

if __name__ == "__main__":
    """
    Runs the FastAPI demo application with uvicorn.
    """
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, log_level="info")