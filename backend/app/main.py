from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db import get_db

app = FastAPI(title="taskpilot API", version="0.1.0")

@app.get("/health")
def health_check():
  return {"status": "ok"}
  
@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
  db.execute(text("SELECT 1"))
  return {"db": "ok"}