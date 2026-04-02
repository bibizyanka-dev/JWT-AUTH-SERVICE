# Auth Service

A small **JWT-based authentication API** built as a learning / portfolio project. It exposes registration, login, and token refresh flows, persists users in **PostgreSQL**, and issues **access** and **refresh** tokens using [fastapi-jwt](https://github.com/k4black/fastapi-jwt).

---

## Features

- **User registration** with email validation and bcrypt-hashed passwords  
- **Login** with username + password  
- **JWT access & refresh** tokens (stateless)  
- **Async** stack: FastAPI + SQLAlchemy 2 + asyncpg  
- **Database migrations** with Alembic  
- **Structured logging** (console + rotating files) with basic sensitive-data filtering  
- **Docker Compose** for local Postgres + API with hot reload  

---

## Tech stack

| Layer        | Choice                          |
|-------------|----------------------------------|
| Framework   | FastAPI                          |
| ORM         | SQLAlchemy 2 (async)             |
| Database    | PostgreSQL 16                    |
| Auth        | JWT (`fastapi-jwt`), bcrypt      |
| Config      | pydantic-settings, `.env`       |
| Migrations  | Alembic                          |

---

## API overview

Base path: **`/api`**

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/auth/registration` | Create account; returns user + tokens |
| `POST` | `/api/auth/login` | Authenticate; returns user + tokens |
| `POST` | `/api/auth/refresh` | New access + refresh pair (send **refresh** JWT in `Authorization: Bearer …`) |

Interactive docs: **`http://localhost:8000/docs`** (Swagger UI).

---

## Token lifetimes (defaults)

Configured in `src/utils/security.py`:

- **Access token:** 24 hours  
- **Refresh token:** 6 days  

Adjust the `timedelta` values there if you need different TTLs.

---

## Prerequisites

- Python **3.12+** (see `Dockerfile`)  
- **Docker** & Docker Compose (recommended), or a local PostgreSQL instance  

---

## Environment variables

Create a **`.env`** file in the project root (never commit real secrets):

| Variable | Description |
|----------|-------------|
| `DB_HOST` | Database host (`localhost` for local Postgres; `postgres` is set by Compose for the app container) |
| `DB_PORT` | Database port (e.g. `5432`) |
| `DB_USER` | Database user |
| `DB_PASS` | Database password |
| `DB_NAME` | Database name |
| `JWT_SECRET` | Secret key used to sign JWTs — use a long, random value in any shared environment |

Example (align credentials with `docker-compose.yaml` if you use the default Postgres service):

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=AuthServiceDB
JWT_SECRET=change-me-to-a-long-random-string
```

---

## Quick start (Docker Compose)

From the repository root:

```bash
docker compose up --build
```

- API: **`http://localhost:8000`**  
- Postgres is exposed on **`localhost:5432`** (default user/db from `docker-compose.yaml`)

Apply migrations **once** (with the stack running and dependencies available), from the project root:

```bash
docker compose exec backend alembic upgrade head
```

Then open **`/docs`** and try the auth endpoints.

---

## Local development (without Docker)

1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

2. Ensure PostgreSQL is running and matches your `.env`.

3. Run migrations:

   ```bash
   alembic upgrade head
   ```

4. Start the app (from project root so `src` imports resolve):

   ```bash
   uvicorn src.main:app --reload --reload-dir src
   ```

---

## Tests

```bash
pytest src/tests -v
```

Tests use an in-memory SQLite database and do not require a running Postgres instance.

---

## Project layout

```text
├── alembic/              # migration scripts
├── src/
│   ├── api/              # HTTP routes
│   ├── database/         # engine, session, settings
│   ├── models/           # SQLAlchemy models
│   ├── repositories/     # data access
│   ├── schemas/          # Pydantic models
│   ├── services/         # business logic
│   ├── utils/            # security, logging, dependencies
│   ├── tests/
│   └── main.py
├── docker-compose.yaml
├── Dockerfile
├── logging_config.yaml
└── requirements.txt
```

---

## Security notes

- This is a **pet / portfolio** service: there is no rate limiting, token revocation store, or OAuth — only stateless JWTs.  
- Use a **strong `JWT_SECRET`** and HTTPS in production.  
- CORS is restricted to local development origins in `src/main.py`; update it for real front-end domains.

---
