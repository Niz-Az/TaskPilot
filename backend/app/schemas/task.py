from pydantic import BaseModel
from typing import Optional
from uuid import UUID 
from datetime import datetime

class TaskCreate(BaseModel):
  title: str
  description: Optional[str] = None

class TaskUpdate(BaseModel):
  title: Optional[str] = None
  description: Optional[str] = None
  completed: Optional[bool] = None

class TaskRead(BaseModel):
  id: UUID
  title: str 
  description: Optional[str]
  completed: bool
  created_at: datetime
  updated_at: datetime 

  class config: 
    from_attributes = True
    

