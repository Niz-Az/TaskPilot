import uuid 
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.sql import func

from app.db import Base

class Task(Base):
  __tablename__ = "tasks"

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  title = Column(String, nullable=False)
  description = Column(String, nullable=True)
  completed = Column(Boolean, default=False, nullable=False)
  owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
  created_at = Column(DateTime(timezone=True), server_default=func.now())
  updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())