import os

# ───────── Auth ─────────
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ───────── Database ─────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://taskpilot:taskpilot@localhost:5433/taskpilot"
)