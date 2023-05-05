"""
schemas.py

This file contains all of the Pydantic schemas used in the application.
"""

# Import modules and libraries
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

from enums import UserType, FireClass, TicketState, TicketType

# User schemas
class UserBase(BaseModel):
    """
    Base properties shared across all User schemas.
    """
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: Optional[UserType] = UserType.user
    is_active: Optional[bool] = True
    is_admin: bool = False

class UserCreate(UserBase):
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserStoredBase(UserBase):
    """
    This represents the base properties of a user stored in the database.
    """
    id: Optional[int] = None

    class Config:
        orm_mode = True

class User(UserStoredBase):
    """
    This is the user class we will be using.
    """
    pass

class UserStoredDatabase(UserStoredBase):
    """
    This represents additional properties of a user stored in the database.
    """
    hashed_password: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None

# Extinguisher schemas
class ExtinguisherBase(BaseModel):
    """
    Properties shared by all extinguisher schemas.
    """
    manufacturer_name: Optional[str] = None
    supplier_name: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[datetime] = None
    extinguisher_type: Optional[FireClass] = FireClass.ABC
    is_active: Optional[bool] = None

class ExtinguisherCreate(ExtinguisherBase):
    manufacturer_name: str
    supplier_name: str
    serial_number: str
    extinguisher_type: FireClass
    is_active: bool

class ExtinguisherUpdate(ExtinguisherBase):
    pass

class Extinguisher(ExtinguisherBase):
    """
    Extinguisher schema.
    """
    id: int

    class Config:
        orm_mode = True

# Ticket schemas
class TicketBase(BaseModel):
    """
    Base properties shared across all of the Ticket schemas.
    """
    ticket_type: Optional[TicketType] = TicketType.other
    ticket_state: Optional[TicketState] = TicketState.open
    title: Optional[str] = "Missing ticket title"
    description: Optional[str] = "Missing ticket description"

class TicketCreate(TicketBase):
    title: str
    description: str

class TicketUpdate(TicketBase):
    pass

class Ticket(TicketBase):
    """
    This represents the base properties of a ticket stored in the database.
    """
    id: int
    assigned_user_id: Optional[int] = None
    related_extinguisher_id: Optional[int] = None
    related_box_id: Optional[int] = None

    class Config:
        orm_mode = True

# Box schemas
class BoxBase(BaseModel):
    """
    Properties shared across all box schemas.
    """
    box_size: Optional[str] = None
    building: Optional[str] = None
    room: Optional[str] = None
    location_description: Optional[str] = None
    is_damaged: Optional[bool] = None

class BoxCreate(BoxBase):
    box_size: str
    building: str
    room: str
    location_description: str
    is_damaged: bool

class BoxUpdate(BoxBase):
    pass

class Box(BoxBase):
    id: int
    extinguishers: List[Extinguisher] = []
    tickets: List[Ticket] = []

    class Config:
        orm_mode = True

# Note schemas
# TODO: Implement note schemas