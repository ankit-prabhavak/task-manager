"""
schemas.py
----------
Defines Pydantic "schemas" - these describe the SHAPE of data going
IN and OUT of the API (JSON), as opposed to models.py which describes
the shape of data in the DATABASE.

Why do we need both models.py AND schemas.py?
- models.py (SQLAlchemy) = database table structure.
- schemas.py (Pydantic)  = API request/response structure.
They usually look similar, but keeping them separate means:
  1. We can validate incoming JSON before it ever touches the DB.
  2. We control exactly what fields get sent back to the frontend
     (e.g. we never let a client set "id" or "created_at" themselves).
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    """Fields the client is allowed to send when creating a task."""
    pass


class TaskUpdate(BaseModel):
    """Fields the client is allowed to send when updating a task."""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskOut(TaskBase):
    """Fields the API sends back to the client."""
    id: int
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True  # lets Pydantic read SQLAlchemy objects directly
