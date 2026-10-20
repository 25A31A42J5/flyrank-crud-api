from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="FlyRank AI CRUD API")
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content={"detail": jsonable_encoder(exc.errors())}
    )

# Request models
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title cannot be empty or contain only spaces")
        return value.strip()


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    done: bool

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Title cannot be empty or contain only spaces")
        return value.strip()


# Welcome endpoint
@app.get("/")
def home():
    return {"message": "Welcome to my FlyRank AI CRUD API!"}


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# In-memory task storage
tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": False},
    {"id": 3, "title": "Build CRUD API", "done": True},
]


# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# Get one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


# Create a task
@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    task = {
        "id": max((task["id"] for task in tasks), default=0) + 1,
        "title": new_task.title,
        "done": False,
    }

    tasks.append(task)
    return task


# Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["done"] = updated_task.done
            return task

    raise HTTPException(status_code=404, detail="Task not found")


# Delete a task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return None

    raise HTTPException(status_code=404, detail="Task not found")