"""
utils.py

Contains utilities for different aspects of the application that I didn't know where else to put.
"""

# Import modules and libraries
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

import crud, models, schemas, config, enums
from database import SessionLocal, engine

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="login/access-token")

def get_database():
    try:
        database = SessionLocal()
        yield database
    finally:
        database.close()

def init_database() -> None:
    """
    Initializes the tables in the database based off the models defined below.
    """
    models.Base.metadata.create_all(bind=engine)

    database_session = SessionLocal()

    # Create the default admin user if they don't already exist
    user = crud.get_user_by_email(database=database_session, user_email=config.DEFAULT_ADMIN_EMAIL)
    if not user:
        new_admin_user = schemas.UserCreate(
            email=config.DEFAULT_ADMIN_EMAIL,
            first_name="ADMIN",
            last_name="DEFAULT",
            user_type=enums.UserType.admin,
            is_active=True,
            is_admin=True,
            password=config.DEFAULT_ADMIN_PASSWORD,
        )
        user = crud.create_user(database=database_session, user_in=new_admin_user)
    
    # Create the default box dubbed warehouse if it doesn't already exist
    warehouse = crud.get_warehouse(database=database_session)
    if not warehouse:
        new_warehouse = schemas.BoxCreate(
            box_size="warehouse",
            building="AHEC Warehouse",
            room="Warehouse",
            location_description="Main warehouse where all extinguishers are stored by default or when in need of repair.",
            is_damaged=False,
        )
        warehouse = crud.create_box(database=database_session, box_in=new_warehouse)

    database_session.close()

def init_test_database_data() -> None:
    """
    Loads demo data into the database to play with the backend with.
    """
    # Create test variables
    test_manager_email = "linda.park@example.com"
    test_manager_first_name = "Linda"
    test_manager_last_name = "Park"
    test_manager_password = "$SuperS3cure2023"
    test_user_email = "santiago.bates@example.com"
    test_user_first_name = "Santiago"
    test_user_last_name = "Bates"
    test_user_password = "$C00lPassword2023"

    database_session = SessionLocal()

    # Create a new manager user to populate the database
    manager_user = crud.get_user_by_email(database=database_session, user_email=test_manager_email)
    if not manager_user:
        new_manager_user_data = schemas.UserCreate(
            email=test_manager_email,
            first_name=test_manager_first_name,
            last_name=test_manager_last_name,
            user_type=enums.UserType.manager,
            is_active=True,
            is_admin=False,
            password=test_manager_password,
        )
        manager_user = crud.create_user(database=database_session, user_in=new_manager_user_data)
    
    # Create a new test user to populate the database
    test_user = crud.get_user_by_email(database=database_session, user_email=test_user_email)
    if not test_user:
        new_test_user_data = schemas.UserCreate(
            email=test_user_email,
            first_name=test_user_first_name,
            last_name=test_user_last_name,
            user_type=enums.UserType.inspector,
            is_active=True,
            is_admin=False,
            password=test_user_password,
        )
        test_user = crud.create_user(database=database_session, user_in=new_test_user_data)

    # Create some test boxes
    for box in range(2, 10):
        test_box = crud.get_box_by_id(database=database_session, box_id=box)
        if not test_box:
            new_box_data = schemas.BoxCreate(
                box_size="standard",
                building="Administration",
                room="24" + str(box),
                location_description="Near room 24" + str(box),
                is_damaged=False,
            )
            test_box = crud.create_box(database=database_session, box_in=new_box_data)

    # Create some test extinguishers
    # 15 is the last number to show that wrong box_ids just get placed into the default warehouse
    for ext in range(2, 15):
        test_ext = crud.get_extinguisher_by_id(database=database_session, extinguisher_id=ext)
        if not test_ext:
            new_test_ext_data = schemas.ExtinguisherCreate(
                manufacturer_name="Advanced Firefighting Systems",
                supplier_name="IgnisPro",
                serial_number="48329" + str(ext),
                purchase_date=datetime.now() ,
                extinguisher_type=enums.FireClass.ABC,
                is_active=True,
            )
            test_ext = crud.create_extinguisher(database=database_session, extinguisher=new_test_ext_data, box_id=ext)

    database_session.close()

def get_current_user(database: Session = Depends(get_database), token: str = Depends(reusable_oauth2)):
    try:
        payload = jwt.decode(token=token, key=config.SECRET_KEY, algorithms=[config.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials!",)
    
    user = crud.get_user_by_id(database=database, user_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found! Sorry.")
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    if not crud.is_user_active(current_user):
        raise HTTPException(status_code=status.HTTP_425_TOO_EARLY, detail="User is inactive! Sorry.")
    return current_user

def get_current_active_admin(current_user: models.User = Depends(get_current_user)):
    if not crud.is_user_admin(current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin! Sorry.")
    return current_user