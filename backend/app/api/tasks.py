from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.core.deps import get_current_user
from typing import List
from fastapi import HTTPException, status
from uuid import UUID 

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskRead)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  task = Task(title = data.title, description = data.description, owner_id = current_user.id)
  db.add(task)
  db.commit()
  db.refresh(task)

  return task

@router.get("", response_model=List[TaskRead])
def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  tasks = (db.query(Task).filter(Task.owner_id == current_user.id).order_by(Task.created_at.desc()).all())

  return tasks

@router.patch("/{task_id}",response_model=TaskRead)
def update_task(task_id: UUID, data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

  task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()

  if not task:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

  if data.title is not None:
    task.title = data.title
  
  if data.description is not None: 
    task.description = data.description
  
  if data.completed is not None: 
    task.completed = data.completed

  db.commit()
  db.refresh(task)
  return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()

  if not task:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

  db.delete(task)
  db.commit()
