import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db
from app.main import app
from fastapi.testclient import TestClient


# 🔑 Override DB for tests
os.environ["DATABASE_URL"] = "postgresql://taskpilot_test:taskpilot_test@localhost:5434/taskpilot_test"

engine = create_engine(os.environ["DATABASE_URL"])

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture
def client():
    return TestClient(app)

app.dependency_overrides[get_db] = override_get_db
