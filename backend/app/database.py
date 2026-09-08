"""
database.py
------------
Sets up the connection to PostgreSQL using SQLAlchemy.

Why this file exists:
- Keeps all "how do we talk to the database" logic in one place.
- Every other file (models.py, routes/tasks.py) imports from here
  instead of creating its own database connection.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# The database connection string comes from an environment variable,
# NOT hardcoded, so we never commit real credentials to Git and so
# the same code works locally, in Docker, and later in EKS.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/taskmanager",
)

# The "engine" is SQLAlchemy's core object that knows how to talk to
# the actual PostgreSQL server.
engine = create_engine(DATABASE_URL)

# A "session" is a temporary workspace used to run queries and commit
# changes. SessionLocal is a factory that creates new sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all our ORM models (see models.py) inherit
# from. SQLAlchemy uses it to know which Python classes map to which
# database tables.
Base = declarative_base()


def get_db():
    """
    A FastAPI "dependency". For every request that needs the database,
    FastAPI will call this function, hand the resulting session to the
    route function, and then make sure it gets closed afterwards -
    even if an error happens.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
