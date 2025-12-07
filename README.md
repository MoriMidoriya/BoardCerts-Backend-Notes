# BoardCerts Backend Assignment

## Overview
This is a backend system built to manage "Notes." The system allows users to Create, Read, Update, and Delete notes using a RESTful API.

The project is built using **FastAPI** for high performance and **MongoDB** for flexible data storage. It focuses on modular design to ensure the codebase is scalable and easy to maintain.

## Features
* **CRUD Operations:** Full support to Create, Read, Update, and List notes.
* **Soft Delete:** When a note is "deleted," it is not removed from the database; instead, a flag (`is_deleted`) is set to true.
* **Audit Logs:** A separate internal logging system records every "CREATE", "UPDATE", and "SOFT_DELETE" action with a timestamp to track activity.
* **Versioning:** The API structure supports versioning (e.g., `/v1/notes`) to allow for future updates without breaking existing integrations.
* **Scalable Architecture:** Logic is separated from API routes to avoid code duplication and allow easier testing.

## Tech Stack
* **Language:** Python 3.x
* **Framework:** FastAPI
* **Database:** MongoDB (using Motor for async connections)
* **Validation:** Pydantic Models
* **Server:** Uvicorn

---

## How to Run the Project

### 1. Prerequisites
* Ensure **Python** is installed.
* Ensure **MongoDB** is running locally on port `27017`.

### 2. Setup Environment
It is recommended to run this project in a virtual environment.

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
````

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Start the Server

Run the following command to start the application with hot-reloading enabled:

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

### 5\. API Documentation

FastAPI provides automatic, interactive documentation. You can test all endpoints directly in your browser:

  * **Swagger UI:** [http://127.0.0.1:8000/docs]

-----

## Architecture & Design Decisions

### 1\. Separation of Concerns (Folder Structure)

The project logic is strictly separated to improve maintainability:

  * **`routes_v1.py`**: Handles API endpoints and HTTP requests only. It does not contain business logic.
  * **`services.py`**: Contains the core business logic (database interactions, audit logging, data processing).
  * **Reasoning:** This allows the logic to be reused across different API versions (v1, v2) without copy-pasting code.

### 2\. Dependency Injection

The project uses FastAPI's `Depends` system for database connections.

  * **Reasoning:** This ensures efficient connection management (opening/closing connections per request) and makes the system easier to test.

### 3\. Pydantic Models

Data validation is handled via `models.py`.

  * **Reasoning:** strict schemas ensure that invalid data never reaches the database and that API responses are consistent.

### 4\. Activity Logging

The system implements a lightweight audit log that writes to a separate collection (`audit_logs`) whenever a write operation occurs.

<!-- end list -->
