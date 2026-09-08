"""
routes/tasks.py
----------------
Defines all the REST API endpoints for tasks:

GET    /api/tasks        -> list all tasks
POST   /api/tasks        -> create a task
PUT    /api/tasks/{id}   -> update a task (e.g. mark completed)
DELETE /api/tasks/{id}   -> delete a task
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[schemas.TaskOut])
def get_tasks(db: Session = Depends(get_db)):
    """Return every task, newest first."""
    return db.query(models.Task).order_by(models.Task.created_at.desc()).all()


@router.post("", response_model=schemas.TaskOut, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task from the JSON body sent by the client."""
    new_task = models.Task(title=task.title, description=task.description)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)  # reloads the object so we get its generated id/created_at
    return new_task


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update fields of an existing task (e.g. mark it completed)."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by id."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return None
