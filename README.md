# Task Manager

A very simple full-stack Task Manager app, built to learn (and later demonstrate)
React, FastAPI, PostgreSQL, Docker, and eventually Kubernetes/EKS on AWS.

## 1. Project Overview

Users can:
- View all tasks
- Create a task (title + optional description)
- Mark a task as completed
- Delete a task

There is intentionally **no authentication, no users, no microservices** —
the goal is to master the fundamentals of a 3-tier web app first.

## 2. Architecture

```
Browser
   |
   v
React (Vite)  --HTTP/JSON-->  FastAPI  --SQL-->  PostgreSQL
(frontend)                    (backend)          (database)
```

- The **frontend** (React) never talks to the database directly.
- The **backend** (FastAPI) is the only thing that talks to PostgreSQL.
- All communication between frontend and backend happens over plain
  REST/JSON via HTTP.

## 3. Technology Stack

| Layer     | Technology                                   |
|-----------|-----------------------------------------------|
| Frontend  | React, Vite, Axios, plain CSS                 |
| Backend   | Python, FastAPI, Uvicorn, SQLAlchemy, Pydantic|
| Database  | PostgreSQL                                    |
| Dev/Ops   | Docker, Docker Compose                        |

## 4. Project Structure

```
task-manager/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app, CORS, startup
│   │   ├── database.py      # DB connection/session setup
│   │   ├── models.py        # SQLAlchemy table definitions
│   │   ├── schemas.py       # Pydantic request/response shapes
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── tasks.py     # /api/tasks endpoints
│   ├── tests/
│   │   └── test_main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main UI component
│   │   ├── main.jsx         # React entry point
│   │   ├── api.js           # Axios calls to backend
│   │   └── App.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .env.example
├── docker-compose.yml
├── .gitignore
├── .env.example
└── README.md
```

## 5. Local Setup (Prerequisites)

- Python 3.12+
- Node.js 20+
- Docker + Docker Compose
- (Optional, if not using Docker for Postgres) PostgreSQL installed locally

## 6. Environment Variables

| File                       | Variable            | Purpose                                  |
|-----------------------------|----------------------|-------------------------------------------|
| `backend/.env`              | `DATABASE_URL`       | Full Postgres connection string           |
| `frontend/.env`             | `VITE_API_URL`       | URL the React app uses to reach FastAPI   |
| `.env` (project root, Compose) | `POSTGRES_DB/USER/PASSWORD`, `VITE_API_URL` | Used by docker-compose.yml |

Copy each `.env.example` to `.env` and adjust if needed:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
cp .env.example .env
```

## 7. Running WITHOUT Docker (local dev)

**Start PostgreSQL** (if you have it installed locally):
```bash
# make sure a database named "taskmanager" exists
createdb taskmanager
```

**Start the backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at http://localhost:8000

**Start the frontend** (in a separate terminal):
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:5173

## 8. Running WITH Docker Compose

From the project root:

```bash
# build and start everything (frontend, backend, postgres)
docker compose up --build

# stop everything
docker compose down

# stop and also delete the database volume (fresh start)
docker compose down -v

# rebuild after code changes
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Postgres: localhost:5432 (mainly for tools like psql/DBeaver)

## 9. API Endpoints

| Method | Endpoint            | Description           |
|--------|----------------------|------------------------|
| GET    | `/health`            | Health check           |
| GET    | `/api/tasks`         | List all tasks         |
| POST   | `/api/tasks`         | Create a task          |
| PUT    | `/api/tasks/{id}`    | Update a task          |
| DELETE | `/api/tasks/{id}`    | Delete a task          |

Example create request:
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker", "description": "Read the docs"}'
```

FastAPI also auto-generates interactive docs at http://localhost:8000/docs

## 10. Running Tests

```bash
cd backend
pip install -r requirements.txt   # if not already installed
pytest
```

## 11. Future AWS/EKS Deployment Architecture (not implemented yet)

```
Internet
   |
   v
AWS Load Balancer / Ingress
   |
   v
React frontend service   (Kubernetes Deployment + Service, in a public subnet)
   |
   v
FastAPI backend service  (Kubernetes Deployment + Service, in a private subnet)
   |
   v
PostgreSQL                (RDS, or a StatefulSet, in a private subnet)
```

Later phases (not part of this project yet) will add: Dockerhub/ECR image
pushes, Kubernetes manifests, an AWS VPC with public/private subnets across
multiple Availability Zones, an Ingress Controller / Application Load
Balancer, and eventually CI/CD.

## How a Request Travels (React → FastAPI → PostgreSQL → FastAPI → React)

1. You click "Add Task" in the browser.
2. React's `handleCreate` calls `createTask()` in `api.js`, which sends
   `POST http://localhost:8000/api/tasks` with a JSON body via Axios.
3. FastAPI's CORS middleware checks that `localhost:5173` is allowed,
   then routes the request to `create_task()` in `routes/tasks.py`.
4. Pydantic (`schemas.TaskCreate`) validates the JSON body's shape.
5. `create_task()` builds a SQLAlchemy `Task` object and calls
   `db.add()` + `db.commit()`, which sends an `INSERT` SQL statement
   to PostgreSQL over the connection defined in `database.py`.
6. PostgreSQL stores the row and returns the generated `id` and
   `created_at`.
7. SQLAlchemy loads those generated values back onto the Python object
   (`db.refresh()`), FastAPI serializes it using `schemas.TaskOut`,
   and sends the JSON response back to the browser.
8. React receives the response, then calls `loadTasks()` again to
   re-fetch the full list and re-render the UI.
