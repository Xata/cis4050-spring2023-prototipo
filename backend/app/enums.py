"""
enums.py

Contains the different types of objects for the application.
"""
# Import modules and libraries
from enum import Enum

class UserType(Enum):
    """
    Represents the different types of users in the application.
    """
    admin = "admin"
    manager = "manager"
    inspector = "inspector"
    maintenance_worker = "maintenance_worker"
    repair_tech = "repair_tech"
    user = "user" # Default value
    archived = "archived"

class FireClass(Enum):
    """
    Represents the common fire types an extinguisher can put out in the United States.
    """
    A = "A" # Ordinary solid combustibles
    B = "B" # Flammable liquids and gases
    C = "C" # Energized electrical equipment
    D = "D" # Combustible metals
    K = "K" # Oils and fats
    ABC = "ABC" # Multi-purpose dry chemical
    other = "other" # Default value

class TicketType(Enum):
    """
    Represents the type of ticket.
    """
    inspect = "inspect"
    damaged_ext = "damaged_ext"
    repair_ext = "repair_ext"
    damaged_box = "damaged_box"
    repair_box = "repair_box"
    other = "other" # Default value

class TicketState(Enum):
    """
    Represents the state of a ticket.
    """
    open = "open"
    in_progress = "in_progress"
    closed = "closed"
    archived = "archived"