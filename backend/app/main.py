"""
main.py
-------
The entry point of the FastAPI application. This is what Uvicorn runs.

Responsibilities:
1. Create the FastAPI app.
2. Configure CORS (so the React dev server is allowed to call this API).
3. Create database tables on startup (fine for a simple learning project;
   in a real production app you'd use a migration tool like Alembic).
4. Register the /health endpoint and the /api/tasks routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routes import tasks

# Creates the "tasks" table in Postgres if it doesn't exist yet.
# This runs once, when the app starts up.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# --- CORS ---
# The browser enforces a security rule called "same-origin policy":
# by default, JavaScript running on http://localhost:5173 (React/Vite)
# is NOT allowed to make requests to http://localhost:8000 (FastAPI)
# because they are different "origins" (different ports).
# CORSMiddleware tells the browser "it's OK, these origins are trusted."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Simple endpoint to confirm the backend is up and reachable."""
    return {"status": "ok"}


# Mount all the /api/tasks routes defined in routes/tasks.py
app.include_router(tasks.router)
