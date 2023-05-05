"""
models.py

This file contains the definitions of the models used in the application.
"""

# Import modules and libraries
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from database import engine
from enums import UserType, FireClass, TicketState, TicketType

# Begin utilities for handling the models
Base = declarative_base()
"""
Creates a base class for all models in the database to inherit from.
"""

# Being all of the application models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(64), unique=True, index=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    user_type = Column(Enum(UserType), default=UserType.user, nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    tickets = relationship("Ticket", back_populates="assigned_user")
    notes = relationship("Note", back_populates="note_created_by")

class Box(Base):
    __tablename__ = "boxes"

    id = Column(Integer, primary_key=True, index=True)
    box_size = Column(String(16), default="standard")
    building = Column(String(32), default="Admin Building")
    room = Column(String(32), default="Missing room data")
    location_description = Column(String(256))
    is_damaged = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    extinguishers = relationship("Extinguisher", back_populates="assigned_box")
    tickets = relationship("Ticket", back_populates="related_box")

class Extinguisher(Base):
    __tablename__ = "extinguishers"

    id = Column(Integer, primary_key=True, index=True)
    manufacturer_name = Column(String(64), default="Missing manufacturer data")
    supplier_name = Column(String(64), default="Missing supplier data")
    serial_number = Column(String, default="Missing serial number data")
    purchase_date = Column(DateTime, default=func.now())
    extinguisher_type = Column(Enum(FireClass), default=FireClass.other, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    assigned_box_id = Column(Integer, ForeignKey("boxes.id"))
    assigned_box = relationship("Box", back_populates="extinguishers")

    tickets = relationship("Ticket", back_populates="related_extinguisher")

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_type = Column(Enum(TicketType), default=TicketType.other, nullable=False)
    ticket_state = Column(Enum(TicketState), default=TicketState.open, nullable=False)
    title = Column(String(64), default="Missing ticket title")

    # Must contain the ID of an extinguisher or box
    description = Column(String(256), default="Missing ticket description")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    assigned_user_id = Column(Integer, ForeignKey("users.id"))
    assigned_user = relationship("User", back_populates="tickets")

    related_extinguisher_id = Column(Integer, ForeignKey("extinguishers.id"), nullable=True)
    related_extinguisher = relationship("Extinguisher", back_populates="tickets")

    related_box_id = Column(Integer, ForeignKey("boxes.id"), nullable=True)
    related_box = relationship("Box", back_populates="tickets")

    notes = relationship("Note", back_populates="ticket")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(256), default="Missing note data")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    ticket = relationship("Ticket", back_populates="notes")

    note_created_by_id = Column(Integer, ForeignKey("users.id"))
    note_created_by = relationship("User", back_populates="notes")
