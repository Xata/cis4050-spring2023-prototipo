"""
security.py

Contains code to handle FastAPI basic security.
"""

# Import modules and libraries
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext

import config

# Define password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""
Password hashing context manager.
"""

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None):
    """Create a new JSON Web Token (JWT) access token.

    Args:
        subject: The subject of the token, typically the user ID.
        expires_delta: The time delta until the token expires.

    Returns:
        str: The encoded JWT access token.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_TIME
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str):
    """Verify that the given plaintext password matches the given hashed password.

    Args:
        plain_password: The plaintext password to be verified.
        hashed_password: The hashed password to be compared against.

    Returns:
        bool: True if the plaintext password matches the hashed password, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    """Return a hashed version of the given plaintext password.

    Args:
        password: The plaintext password to be hashed.

    Returns:
        str: The hashed version of the password.
    """
    return pwd_context.hash(password)
