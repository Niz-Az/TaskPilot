from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead
from app.core.deps import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskRead)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  task = Task(title = data.title, description = data.description, owner_id = current_user.id)
  db.add(task)
  db.commit()
  db.refresh(task)

  return task