"""
user_router.py

This file contains all the routes for the user objects.
"""

# Import modules and libraries
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import schemas, models, crud, utils

router = APIRouter()
"""
Instance of a router that handles all user requests and responses for the app.
"""

@router.get("/", response_model=List[schemas.User])
def read_users(database: Session = Depends(utils.get_database), offset: int = 0, limit: int = 16, current_user: models.User = Depends(utils.get_current_active_admin)):
    """
    This function pulls a list of users from the database.
    """
    users = crud.get_users(database=database, offset=offset, limit=limit)
    return users

@router.post("/", response_model=schemas.User)
def create_user(database: Session = Depends(utils.get_database), new_user: schemas.UserCreate = None, current_user: models.User = Depends(utils.get_current_active_admin)):
    """
    Creates a new user in the database.
    """
    user = crud.get_user_by_email(database=database, user_email=new_user.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists! Sorry.")
    else:
        user = crud.create_user(database=database, user_in=new_user)
        return user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(database: Session = Depends(utils.get_database), user_id: int = 0, new_user: schemas.UserUpdate = None, current_user: models.User = Depends(utils.get_current_active_admin)):
    """
    Update a user with admin credentials.
    """
    if current_user.is_admin is False:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied to edit user!")

    user = crud.get_user_by_id(database=database, user_id=user_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user does not exist!")
    
    user = crud.update_user(database=database, user=user, user_updates=new_user)
    return user

@router.put("/me", response_model=schemas.User)
def update_user_me(database: Session = Depends(utils.get_database), new_password: str = Body(None), new_first_name: str = Body(None), new_last_name: str = Body(None), current_user: models.User = Depends(utils.get_current_active_user)):
    """
    Allows the user to make changes to self. For the frontend "settings" section.
    User does not have to be admin.
    """
    current_user_data = jsonable_encoder(current_user)
    new_user_data = schemas.UserUpdate(**current_user_data)

    if new_password is not None:
        new_user_data.password = new_password
    
    if new_first_name is not None:
        new_user_data.first_name = new_first_name

    if new_last_name is not None:
        new_user_data.last_name = new_last_name

    user = crud.update_user(database=database, user=current_user, user_updates=new_user_data)
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="There was an unknown error!")
