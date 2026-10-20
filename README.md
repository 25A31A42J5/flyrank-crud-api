# FlyRank AI CRUD API

A simple REST API built with **Python and FastAPI** as part of the FlyRank AI internship assignment.

This project demonstrates CRUD (Create, Read, Update, Delete) operations for managing tasks, with automatic ID generation, input validation, and HTTP error handling.

## Features

* Create, retrieve, update, and delete tasks.
* Automatically generate unique task IDs.
* Default new tasks to `done: false`.
* Validate task titles and reject empty or whitespace-only values.
* Return appropriate HTTP status codes.
* Store tasks in memory.
* Explore and test endpoints through Swagger UI.

## Technologies Used

* Python
* FastAPI
* Pydantic
* Uvicorn
* Git and GitHub

## Getting Started

### Prerequisites

* Python 3.10 or later
* pip

### 1. Clone the repository

```bash
git clone https://github.com/25A31A42J5/flyrank-crud-api.git
cd flyrank-crud-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install "fastapi[standard]"
```

### 4. Start the server

```bash
python -m uvicorn main:app --reload
```

The API will be available at:

* **Base URL:** http://127.0.0.1:8000
* **Swagger UI:** http://127.0.0.1:8000/docs
* **ReDoc:** http://127.0.0.1:8000/redoc
* **Health check:** http://127.0.0.1:8000/health

## API Endpoints

| Method | Endpoint           | Description           | Success Status |
| ------ | ------------------ | --------------------- | -------------- |
| GET    | `/`                | Welcome message       | 200 OK         |
| GET    | `/health`          | Check API health      | 200 OK         |
| GET    | `/tasks`           | Retrieve all tasks    | 200 OK         |
| GET    | `/tasks/{task_id}` | Retrieve a task by ID | 200 OK         |
| POST   | `/tasks`           | Create a task         | 201 Created    |
| PUT    | `/tasks/{task_id}` | Update a task         | 200 OK         |
| DELETE | `/tasks/{task_id}` | Delete a task         | 204 No Content |

## Example Requests

### Create a task

**POST** `/tasks`

Request body:

```json
{
  "title": "Learn FastAPI"
}
```

Example successful response (`201 Created`):

```json
{
  "id": 4,
  "title": "Learn FastAPI",
  "done": false
}
```

The generated ID may differ depending on the current task list.

### Update a task

**PUT** `/tasks/1`

Request body:

```json
{
  "title": "Complete the CRUD API",
  "done": true
}
```

### Retrieve all tasks

**GET** `/tasks`

Example response:

```json
[
  {
    "id": 1,
    "title": "Learn Python",
    "done": false
  },
  {
    "id": 2,
    "title": "Learn FastAPI",
    "done": false
  },
  {
    "id": 3,
    "title": "Build CRUD API",
    "done": true
  }
]
```

### Delete a task

**DELETE** `/tasks/1`

A successful deletion returns `204 No Content` with an empty response body.

## Validation and Error Handling

| Status Code     | Meaning                                           |
| --------------- | ------------------------------------------------- |
| 400 Bad Request | Invalid request data, such as an empty task title |
| 404 Not Found   | The requested task ID does not exist              |
| 201 Created     | A task was successfully created                   |
| 204 No Content  | A task was successfully deleted                   |

Task titles cannot be empty or contain only whitespace. Valid titles are trimmed before storage.

## Storage

Tasks are stored in an in-memory Python list. No external database is required.

**Note:** Tasks created or modified while the server is running are not persisted. Restarting the server restores the initial sample tasks.

## Testing

The API can be tested interactively using Swagger UI at `/docs`.

Command-line example:

```bash
curl -i http://127.0.0.1:8000/health
```

Include the actual output from running this command in the project README before submission.

## Project Repository

GitHub: https://github.com/25A31A42J5/flyrank-crud-api

## Author

Developed as part of the FlyRank AI internship assignment.
