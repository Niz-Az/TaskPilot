from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user
from app.models.user import User
from fastapi.middleware.cors import CORSMiddleware



from sqlalchemy import text

from app.db import get_db

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router


app = FastAPI(title="taskpilot API", version="0.1.0")
app.include_router(auth_router)
app.include_router(tasks_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/health")
def health_check():
  return {"status": "ok"}
  
@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
  db.execute(text("SELECT 1"))
  return {"db": "ok"}

@app.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
  return {"id": str(current_user.id), "email": current_user.email}


