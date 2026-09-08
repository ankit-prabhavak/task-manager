"""
models.py
---------
Defines the database TABLE structure using SQLAlchemy's ORM.

An ORM (Object Relational Mapper) lets us describe a database table
as a normal Python class. SQLAlchemy translates that class into SQL
CREATE TABLE statements and translates rows into Python objects.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
