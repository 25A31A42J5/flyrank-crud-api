from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
class TaskCreate(BaseModel):
    title: str = Field(min_length=1)
class TaskUpdate(BaseModel):
    title: str = Field(min_length=1)
    done: bool


@app.get("/")
def home():
    return {"message": "Welcome to my FlyRank AI CRUD API!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

tasks = [
    {"id": 1, "title": "Learn Python", "done": False},
    {"id": 2, "title": "Learn FastAPI", "done": False},
    {"id": 3, "title": "Build CRUD API", "done": True}
]


@app.get("/tasks")
def get_tasks():
    return tasks
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    task = {
        "id": max(task["id"] for task in tasks) + 1,
        "title": new_task.title,
        "done": False
    }
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = updated_task.title
            task["done"] = updated_task.done
            return task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {
                "message": "Task deleted successfully",
                "task": task
            }

    raise HTTPException(status_code=404, detail="Task not found")

    raise HTTPException(status_code=404, detail="Task not found")

    tasks.append(task)
    return task

    raise HTTPException(status_code=404, detail="Task not found")