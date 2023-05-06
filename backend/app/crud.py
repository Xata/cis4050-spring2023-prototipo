"""
crud.py

This Python file contains all of the business logic for the models in the database.
"""

# Import modules and libraries
from typing import Any, Dict, Optional, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from security import get_password_hash, verify_password
import database
import models
import schemas

# User CRUD operations
def is_user_active(user: models.User) -> bool:
    return user.is_active

def is_user_admin(user: models.User) -> bool:
    return user.is_admin

def authenticate_user(database: Session, email: str, password: str):
    user = get_user_by_email(database=database, user_email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    else:
        return user

def get_users(database: Session, offset: int = 0, limit: int = 100):
    return database.query(models.User).offset(offset).limit(limit).all()

def get_user_by_id(database: Session, user_id: int):
    return database.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(database: Session, user_email: str):
    return database.query(models.User).filter(models.User.email == user_email).first()

def create_user(database: Session, user_in: schemas.UserCreate):
    new_user = models.User(
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_admin=user_in.is_admin,
        user_type=user_in.user_type,
    )
    database.add(new_user)
    database.commit()
    database.refresh(new_user)
    return new_user

def update_user(database: Session, user: models.User, user_updates: Union[schemas.UserUpdate, Any]):
    """
    This updates a user in the database.
    """
    # Check if the correct data is being passed through
    if isinstance(user_updates, dict):
        user_update_data = user_updates
    else:
        # Exclude any unset data
        user_update_data = user_updates.dict(exclude_unset=True)
    
    # If the schema provided a new password then hash it and discard the user input
    if user_update_data["password"]:
        new_hashed_password = get_password_hash(user_update_data["password"])
        del user_update_data["password"]
        user_update_data["hashed_password"] = new_hashed_password
    
    # Convert the currect user data into JSON
    user_data = jsonable_encoder(user)

    # Update the data
    for field in user_data:

        # If field has a value then update it
        if field in user_update_data:
            setattr(user, field, user_update_data[field])

    # Commit the changes to the database
    database.add(user)
    database.commit()
    database.refresh(user)
    return user

def delete_user():
    pass

# Box CRUD operations
def get_boxes(database: Session, offset: int = 0, limit: int = 100):
    return database.query(models.Box).offset(offset).limit(limit).all()

def get_box_by_id(database: Session, box_id: int):
    return database.query(models.Box).filter(models.Box.id == box_id).first()

def get_box_by_building(database: Session, box_building: str):
    return database.query(models.Box).filter(models.Box.building == box_building).first()

def get_warehouse(database: Session):
    return database.query(models.Box).filter(models.Box.box_size == "warehouse").first()

def create_box(database: Session, box_in: schemas.BoxCreate):
    new_box = models.Box(
        box_size = box_in.box_size,
        building = box_in.building,
        room = box_in.room,
        location_description = box_in.location_description,
        is_damaged = box_in.is_damaged,
    )
    database.add(new_box)
    database.commit()
    database.refresh(new_box)
    return new_box

def update_box(database: Session, box_id: int, box: schemas.BoxUpdate):
    database_box = get_box_by_id(database=database, box_id=box_id)
    if database_box:
        update_data = box.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(database_box, field, value)
        database.commit()
        database.refresh(database_box)
        return database_box

def delete_box():
    pass

# Extinguisher CRUD operations
def get_extinguishers(database: Session, offset: int = 0, limit: int = 100):
    """
    Get a list of extinguishers from the database.
    """
    return database.query(models.Extinguisher).offset(offset).limit(limit).all()

def get_extinguisher_by_id(database: Session, extinguisher_id: int):
    """
    Retrieve an extinguisher by ID.
    """
    return database.query(models.Extinguisher).filter(models.Extinguisher.id == extinguisher_id).first()

def get_extinguishers_by_type(database: Session, extinguisher_type: str, offset: int = 0, limit: int = 100):
    return database.query(models.Extinguisher).filter(models.Extinguisher.extinguisher_type == extinguisher_type).offset(offset).limit(limit).all()

def get_extinguisher_type_list(database: Session):
    return database.query(models.Extinguisher.extinguisher_type).distinct().all()

def create_extinguisher(database: Session, extinguisher: schemas.ExtinguisherCreate, box_id: int):
    box = database.query(models.Box).filter(models.Box.id == box_id).first()
    # If the box doesn't exist put the extinguisher in the default box (warehouse)
    if not box:
        database_extinguisher = models.Extinguisher(**extinguisher.dict())
        database_extinguisher.assigned_box_id = 1
        database.add(database_extinguisher)
        database.commit()
        database.refresh(database_extinguisher)
        return database_extinguisher
    else:
        database_extinguisher = models.Extinguisher(**extinguisher.dict())
        database_extinguisher.assigned_box_id = box_id
        database.add(database_extinguisher)
        database.commit()
        database.refresh(database_extinguisher)
        return database_extinguisher

def delete_extinguisher_by_id(database: Session, extinguisher_id: int):
    extinguisher = database.query(models.Extinguisher).filter_by(id=extinguisher_id).first()
    if extinguisher:
        extinguisher.is_active = False
        extinguisher.box_id = 1
        database.commit() 
        database.refresh(extinguisher)
        return extinguisher
    else:
        return None

# Ticket CRUD operations
# TODO: Implement the ticket system
def get_tickets():
    pass

def create_ticket():
    pass

def update_ticket_status():
    pass



