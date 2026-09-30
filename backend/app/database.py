# Backward-compatible imports. The application uses app.database.connection and app.database.database.
from .database.connection import engine
from .database.database import Base, SessionLocal, get_db

__all__ = ["engine", "Base", "SessionLocal", "get_db"]
