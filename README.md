# TaskPilot

## Overview
TaskPilot is a full-stack task management project built around a FastAPI backend and a React frontend. It solves the core workflow of personal task tracking with secure authentication and per-user task isolation, so each authenticated user can manage only their own tasks.

The repository is designed like a portfolio-ready backend-focused system: JWT auth, relational data modeling, database migrations, API testing, and a lightweight frontend login flow.

## Features
- User registration and login with JWT access tokens.
- Protected API endpoints using Bearer token authentication.
- Create, list, update, and delete tasks.
- User-scoped task ownership (users only access their own tasks).
- PostgreSQL-backed persistence with SQLAlchemy models.
- Alembic migration history for schema evolution.
- Health and database connectivity checks (`/health`, `/db-check`).
- Docker Compose setup for local development and isolated test database instances.

## Tech Stack
### Backend
- Python 3
- FastAPI
- SQLAlchemy
- PostgreSQL (via `psycopg2-binary`)
- Alembic migrations
- Pydantic
- JWT authentication (`python-jose`)
- Password hashing (`passlib` + `bcrypt`)
- Pytest

### Frontend
- React
- Vite
- JavaScript (ES modules)

### DevOps / Tooling
- Docker Compose (Postgres services)
- Uvicorn (ASGI server)

## Architecture
TaskPilot follows a clear layered structure:

- **API Layer (`backend/app/api`)**: FastAPI routers define auth and task endpoints.
- **Domain/Data Layer (`backend/app/models`, `backend/app/schemas`)**: SQLAlchemy models define persistence; Pydantic schemas define request/response contracts.
- **Infrastructure Layer (`backend/app/db.py`, `backend/alembic`)**: Database session management and schema migrations.
- **Security Layer (`backend/app/core`)**: JWT creation/validation, password hashing, and current-user dependency injection.
- **Frontend Layer (`frontend/src`)**: Minimal React client for login and authenticated API calls.

### Authentication design
- Login/register endpoints return JWT bearer tokens.
- Protected routes use a reusable dependency (`get_current_user`) that decodes the token and resolves the user from the database.

### Data ownership model
- Every task is linked to a user (`owner_id` FK).
- Task routes always filter by authenticated user ID to enforce data isolation.

## Repository Structure
```text
TaskPilot/
├── backend/
│   ├── app/
│   │   ├── api/            # FastAPI route handlers (auth, tasks)
│   │   ├── core/           # Config, JWT, password hashing, auth dependencies
│   │   ├── models/         # SQLAlchemy models (User, Task)
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── db.py           # Engine, SessionLocal, Base, DB dependency
│   │   └── main.py         # FastAPI app entrypoint and router registration
│   ├── alembic/            # Migration environment and revision scripts
│   ├── tests/              # API tests for auth and tasks
│   ├── requirements.txt    # Python dependencies
│   └── alembic.ini         # Alembic configuration
├── frontend/
│   ├── src/
│   │   ├── api/            # Fetch client and token handling
│   │   ├── auth/           # Login UI + auth API integration
│   │   ├── App.jsx         # Root UI flow (login state)
│   │   └── main.jsx        # React bootstrap
│   ├── package.json        # Node dependencies and scripts
│   └── vite.config.js      # Vite config
├── docker-compose.yml      # Local Postgres services (dev + test)
└── README.md
```

## API Overview
Base URL (local): `http://127.0.0.1:8000`

### Public routes
- `POST /auth/register` — register a new user, returns JWT token.
- `POST /auth/login` — authenticate user, returns JWT token.
- `GET /health` — API health check.
- `GET /db-check` — confirms database connectivity.

### Protected routes (Bearer token required)
- `GET /me` — returns current user identity.
- `POST /tasks` — create a task.
- `GET /tasks` — list tasks for the current user.
- `PATCH /tasks/{task_id}` — update a task.
- `DELETE /tasks/{task_id}` — delete a task.

## Getting Started

### Prerequisites
- Python 3.11+ (recommended)
- Node.js 18+ and npm
- Docker + Docker Compose

### 1) Clone the repository
```bash
git clone <your-repo-url>
cd TaskPilot
```

### 2) Start PostgreSQL services
```bash
docker compose up -d
```

This starts:
- `taskpilot_db` on `localhost:5433` (development)
- `taskpilot_db_test` on `localhost:5434` (testing)

### 3) Configure backend environment variables
Create a `.env` file (or export variables in your shell) for backend runtime:

```env
DATABASE_URL=postgresql://taskpilot:taskpilot@localhost:5433/taskpilot
SECRET_KEY=change-this-in-production
```

### 4) Install backend dependencies
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 5) Run database migrations
```bash
alembic upgrade head
```

### 6) Start the backend server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7) Start the frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```

Frontend default URL: `http://localhost:5173`

## Example Usage

### Register
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Create a task (authenticated)
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"title":"Ship TaskPilot README","description":"Polish docs for recruiters"}'
```

## Future Improvements
- Add full frontend dashboard (task list, filters, status toggles, CRUD UI).
- Add token refresh and logout invalidation strategy.
- Add role support and team/shared-workspace capabilities.
- Add due dates, priorities, labels, and search.
- Add background notifications/reminders.
- Add CI pipeline (lint + test + migration checks).
- Add production deployment manifests (e.g., Render/Fly.io/AWS + managed Postgres).

## Author
Developed by **Nizar Azmi**  
Software Engineering Student – **McGill University**
