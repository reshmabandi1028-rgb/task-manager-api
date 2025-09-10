# tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from . import models, schemas, database, auth

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Create a task ---
@router.post("/", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_task = models.Task(**task.dict(), user_id=current_user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    logger.info(f"Task created: {db_task.title} by {current_user.username}")
    return db_task

# --- Get all tasks ---
@router.get("/", response_model=list[schemas.Task])
def read_tasks(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    tasks = db.query(models.Task).filter(models.Task.user_id == current_user.id).all()
    logger.info(f"User {current_user.username} retrieved {len(tasks)} tasks")
    return tasks

# --- Get single task ---
@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if not task:
        logger.warning(f"Task {task_id} not found for user {current_user.username}")
        raise HTTPException(status_code=404, detail="Task not found")

    logger.info(f"Task {task_id} retrieved by {current_user.username}")
    return task

# --- Update a task ---
@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task_update: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if not db_task:
        logger.warning(f"Update failed: Task {task_id} not found for {current_user.username}")
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.title = task_update.title
    db_task.description = task_update.description
    db.commit()
    db.refresh(db_task)

    logger.info(f"Task {task_id} updated by {current_user.username}")
    return db_task

# --- Delete a task ---
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == current_user.id
    ).first()

    if not db_task:
        logger.warning(f"Delete failed: Task {task_id} not found for {current_user.username}")
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()

    logger.info(f"Task {task_id} deleted by {current_user.username}")
    return None
