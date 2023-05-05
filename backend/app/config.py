"""
config.py

This contains the code to load configuration and environment settings for the backend app.
"""

# Import modules and libraries


# General app settings
APP_TITLE = "Fire Extinguisher Management System"
APP_DESCRIPTION = "An application to demonstrate the hypothetical AHEC Fire Extinguisher Management System!"
APP_VERSION = "0.0.1"
APP_HOST = "127.0.0.1"
APP_PORT = 8083
LOG_LEVEL = "info"

# Database settings
SQLITE_DATABASE_PATH = "sqlite:///./backend/app/extinguisher_demo_app.sqlite"
"""
A string that specifies the path to the SQLite database file used.
"""

# Security Settings
SECRET_KEY = "teamasti2023"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_TIME = int(60)

# Default admin configuration
DEFAULT_ADMIN_EMAIL = "admin@example.com"
DEFAULT_ADMIN_PASSWORD = "$TeamAsti2023"