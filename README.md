# Core API

A reusable backend foundation built with FastAPI and PostgreSQL for developing secure, scalable, and maintainable business applications.

## Features

- JWT Authentication
- Refresh Tokens
- Argon2 Password Hashing
- Role-Based Access Control (RBAC)
- Users & People Management
- Roles & Permissions Management
- User Roles Assignment
- Role Permissions Assignment
- User Profile
- Notification Module
- Audit Fields
- Soft Delete
- Pagination
- UUID Primary Keys
- Alembic Migrations
- PostgreSQL
- OpenAPI / Swagger Documentation

---

## Technology Stack

- Python 3.14
- FastAPI
- SQLAlchemy 2.x
- PostgreSQL
- Alembic
- Pydantic v2
- JWT
- Argon2
- Uvicorn

---

## Project Structure

```
app/
├── api/
├── core/
├── db/
├── models/
├── schemas/
├── seeders/
├── services/
├── utils/
└── main.py
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/your-user/core.git
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

Example:

```env
APP_NAME=Core API

SECRET_KEY=CHANGE_ME

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/core

CORE_SCHEMA=core
```

---

## Database

Run migrations

```bash
alembic upgrade head
```

Run seeders

```bash
python -m app.seeders.run
```

---

## Run

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

Redoc

```
http://127.0.0.1:8000/redoc
```

---

## Current Modules

- Authentication
- Register
- Profile
- People
- Users
- Roles
- Permissions
- Role Permissions
- User Roles
- Notifications

---

## Roadmap

- File Management
- WebSockets
- Redis Cache
- Background Jobs
- Internationalization (i18n)
- Automated Tests
- Docker Support

---

## License

MIT License
