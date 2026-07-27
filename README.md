# Workout Tracker API

A RESTful API built with **Flask** that allows users to manage workouts, exercises, and workout routines. The application provides endpoints for creating, retrieving, and deleting workouts and exercises, while allowing exercises to be associated with specific workouts.

The project demonstrates backend development practices including relational database design, ORM usage, API validation, database migrations, and automated testing.

---

# Table of Contents

* [Project Overview](#project-overview)
* [Features](#features)
* [Technology Stack](#technology-stack)
* [System Architecture](#system-architecture)
* [Project Structure](#project-structure)
* [Database Design](#database-design)
* [Installation](#installation)
* [Database Setup](#database-setup)
* [Running the Application](#running-the-application)
* [API Documentation](#api-documentation)
* [Testing](#testing)
* [Validation and Error Handling](#validation-and-error-handling)
* [Future Improvements](#future-improvements)
* [Author](#author)
* [License](#license)

---

# Project Overview

Workout Tracker API is a backend application designed to help users organize and track their workout routines.

The system manages:

* Workouts
* Exercises
* Workout-exercise relationships

The API follows REST principles and uses a relational database model where exercises can be connected to workouts through an association table containing additional workout-specific information such as sets, repetitions, and duration.

---

# Features

## Workout Management

* Create workouts
* Retrieve all workouts
* Retrieve a single workout by ID
* Delete workouts

## Exercise Management

* Create exercises
* Retrieve all exercises
* Retrieve a single exercise by ID
* Delete exercises

## Workout Routine Management

* Add exercises to workouts
* Store exercise details:

  * Number of sets
  * Number of repetitions
  * Duration

## Backend Features

* RESTful API design
* SQLAlchemy ORM integration
* Database migrations using Alembic
* Request validation using Marshmallow
* Database constraints
* Error handling
* Automated testing using Pytest

---

# Technology Stack

## Backend

| Technology       | Purpose                      |
| ---------------- | ---------------------------- |
| Python           | Programming language         |
| Flask            | Web framework                |
| Flask-SQLAlchemy | ORM integration              |
| SQLAlchemy       | Database modelling           |
| Flask-Migrate    | Database migrations          |
| Alembic          | Migration management         |
| Marshmallow      | Serialization and validation |
| Pytest           | Automated testing            |

## Database

* SQLite (development database)

---

# System Architecture

The application follows a layered backend structure:

```
Client
  |
  |
Flask REST API
  |
  |
Schemas (Validation + Serialization)
  |
  |
SQLAlchemy Models
  |
  |
SQLite Database
```

---

# Project Structure

```
workout-api/

├── README.md
├── requirements.txt
├── .gitignore
│
├── migrations/
│   └── versions/
│
├── tests/
│   ├── conftest.py
│   ├── test_workouts.py
│   ├── test_exercises.py
│   └── test_workoutexercises.py
│
└── server/
    ├── app.py
    ├── models.py
    ├── schemas.py
    ├── seed.py
    ├── config.py
    └── instance/
        └── app.db
```

---

# Database Design

The application uses three main tables.

## Workouts

Stores workout information.

Fields:

* id
* date
* duration_minutes
* notes

## Exercises

Stores available exercises.

Fields:

* id
* name
* category
* equipment_needed

## Workout Exercises

Association table between workouts and exercises.

Fields:

* id
* workout_id
* exercise_id
* sets
* reps
* duration_seconds

Relationship:

```
Workout
   |
   | one-to-many
   |
WorkoutExercise
   |
   | many-to-one
   |
Exercise
```

---

# Installation

## 1. Clone the Repository

```bash
git clone git@github.com:mosweta-school/Workout-API.git

cd workout-api
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Linux/macOS

```bash
source venv/bin/activate
```


---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Database Setup

Initialize and apply migrations:

```bash
flask db upgrade
```

To populate sample data:

```bash
python -m server.seed
```

---

# Running the Application

Start the Flask server:

```bash
python -m server.app
```

The API will run at:

```
http://127.0.0.1:5555
```

Test the API:

```
GET /
```

Response:

```json
{
    "message": "workout tracker API is running"
}
```

---

# API Documentation

## Workouts

### Get All Workouts

```
GET /workouts
```

Response:

```json
[
    {
        "id": 1,
        "date": "2026-07-27",
        "duration_minutes": 60,
        "notes": "Upper body workout"
    }
]
```

---

### Get Single Workout

```
GET /workouts/<id>
```

Example:

```
GET /workouts/1
```

---

### Create Workout

```
POST /workouts
```

Request:

```json
{
    "date": "2026-07-27",
    "duration_minutes": 45,
    "notes": "Morning workout"
}
```

Response:

```json
{
    "id": 1,
    "date": "2026-07-27",
    "duration_minutes": 45,
    "notes": "Morning workout"
}
```

---

### Delete Workout

```
DELETE /workouts/<id>
```

---

# Exercises

## Get All Exercises

```
GET /exercises
```

---

## Get Single Exercise

```
GET /exercises/<id>
```

---

## Create Exercise

```
POST /exercises
```

Request:

```json
{
    "name": "Deadlift",
    "category": "Strength",
    "equipment_needed": true
}
```

---

## Delete Exercise

```
DELETE /exercises/<id>
```

---

# Workout Exercises

## Add Exercise To Workout

```
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
```

Example:

```
POST /workouts/1/exercises/2/workout_exercises
```

Request:

```json
{
    "sets": 3,
    "reps": 12,
    "duration_seconds": null
}
```

Response:

```json
{
    "id": 1,
    "workout_id": 1,
    "exercise_id": 2,
    "sets": 3,
    "reps": 12,
    "duration_seconds": null
}
```

---

# Testing

The project uses **Pytest** for automated testing.

Run:

```bash
pytest
```

Expected output:

```
21 passed
```

Tests cover:

* Workout endpoints
* Exercise endpoints
* Workout-exercise relationships
* Validation failures
* Database constraints
* Error responses

---

# Validation and Error Handling

The API includes validation at multiple levels.

## Marshmallow Validation

Handles:

* Required fields
* Data types
* Request validation

Example:

```json
{
    "errors": {
        "duration_minutes": [
            "Missing data for required field."
        ]
    }
}
```

---

## Database Constraints

Examples:

* Exercise names must be unique
* Workout-exercise combinations cannot be duplicated

Example:

```json
{
    "error": "Exercise already exists in this workout."
}
```

---

## Screenshots
### Tests
<img width="1243" height="291" alt="image" src="https://github.com/user-attachments/assets/fa9d5065-be94-4e82-b68b-d700638e9c17" />

### Postman testing
<img width="1075" height="951" alt="image" src="https://github.com/user-attachments/assets/84b25f3a-d802-49e7-a62e-6b0ee4109d80" />

# GitHub topics

```
python
flask
rest-api
sqlalchemy
sqlite
pytest
backend
api
```


# Future Improvements

Potential improvements for future versions:

## Authentication

* User accounts
* JWT authentication
* Personal workout ownership

## API Improvements

* Update endpoints (`PUT/PATCH`)
* Pagination
* Filtering
* Search functionality
* Swagger/OpenAPI documentation

## Deployment

* PostgreSQL production database
* Docker containerization
* Cloud deployment
* CI/CD pipeline

## Frontend

A React frontend could be added to provide:

* Workout dashboard
* Progress tracking
* Exercise library
* Analytics

---

# Author

Deogracious Moriasi

Backend Developer | Flask | Python | REST APIs

---

# License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project with attribution.
