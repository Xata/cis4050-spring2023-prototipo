"""
database.py
This Python file contains code to create and manage database connections and sessions.
"""

# Import modules nad libraries
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLITE_DATABASE_PATH

engine = create_engine(SQLITE_DATABASE_PATH , connect_args={"check_same_thread": False})
"""
Creates a SQLAlchemy engine for connecting to the SQLite database.
"""

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
Creates a factory function for creating SQLAlchemy database sessions.
"""