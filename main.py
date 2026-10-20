import sqlite3

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="FlyRank AI CRUD API")

DATABASE = "tasks.db"


# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create database table and seed initial tasks
def initialize_database():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
        """)

        count = conn.execute(
            "SELECT COUNT(*) FROM tasks"
        ).fetchone()[0]

        if count == 0:
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                [
                    ("Learn Python", 0),
                    ("Learn FastAPI", 0),
                    ("Build CRUD API", 1),
                ],
            )


initialize_database()


# Preserve Assignment 1 validation behaviour
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=400,
        content={"detail": jsonable_encoder(exc.errors())},
    )


# Request models
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                "Title cannot be empty or contain only spaces"
            )
        return value.strip()


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    done: bool

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(
                "Title cannot be empty or contain only spaces"
            )
        return value.strip()


# Welcome endpoint
@app.get("/")
def home():
    return {"message": "Welcome to my FlyRank AI CRUD API!"}


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Get all tasks from SQLite
@app.get("/tasks")
def get_tasks():
    with get_db_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks"
        ).fetchall()

        return [
            {
                "id": row["id"],
                "title": row["title"],
                "done": bool(row["done"]),
            }
            for row in rows
        ]


# Get one task from SQLite
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        return {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"]),
        }


# Create, update, and delete will be connected in Stages 2 and 3.
