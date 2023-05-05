"""
login_router.py

Handles login requests to the backend.
"""

# Import modules and libraries
from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schemas, models, crud, utils, config,security

router = APIRouter()
"""
Instance of a router that handles all login requests and responses for the app.
"""

@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(database: Session = Depends(utils.get_database), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.authenticate_user(database=database, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    elif not crud.is_user_active(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_TIME)
    return {"access_token": security.create_access_token(user.id, expires_delta=access_token_expires), "token_type": "bearer",}

@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(utils.get_current_user)):
    """
    Test access token
    """
    return current_user