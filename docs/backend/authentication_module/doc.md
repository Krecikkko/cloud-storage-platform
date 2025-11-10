# Authentication Module

This is a documentation for the **User Authentication and Authorization** module.
Person responsible for the documentation of this module is **Laura Gabryjańczyk**.

---

## Setup & Configuration

### Environment

The authentication module is part of the backend system built with **FastAPI** and **SQLAlchemy**.
To run it locally, the following components are required:

* Python **3.10+**
* `pip` and `virtualenv`

### Project structure

The module is located in the main backend application under:

```
backend/app/
├── main.py
├── db.py
├── models/
│   └── user.py
├── routes/
│   └── auth.py
├── schemas/
│   ├── auth.py
│   ├── user.py
│   └── me.py
└── utils/
    ├── security.py
    ├── auth_deps.py
    └── config.py
```

### Installation

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Database

The module uses **SQLAlchemy** with asynchronous sessions.
Default development configuration uses **SQLite**.
The database file is automatically created after the first run.

To create tables:

```bash
alembic upgrade head
```

### Running the server

From the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

After startup, open [http://localhost:8000/docs](http://localhost:8000/docs) to access Swagger UI.

---

## User Management

Users are registered and authenticated using JWT tokens.
Each user has a defined role:

* `user` – standard access (default)
* `admin` – extended permissions (protected routes)

### User data storage

User records are stored in the `users` table with the following schema:
![image](users_table.png)

| Field             | Type                  | Description                   |
| ----------------- | --------------------- | ----------------------------- |
| `id`              | Integer (PK)          | Unique user ID                |
| `username`        | String                | Unique username               |
| `email`           | String                | Unique email address          |
| `hashed_password` | String                | Hashed password using bcrypt  |
| `role`            | Enum(`admin`, `user`) | User role in the system       |
| `created_at`      | DateTime              | Timestamp of account creation |

---

## JWT Authentication

The authentication system uses JSON Web Tokens (**JWT**) for secure user sessions.

### Token characteristics

| Property   | Description                               |
| ---------- | ----------------------------------------- |
| Algorithm  | `HS256`                                   |
| Secret key | Defined in `app/utils/config.py`          |
| Expiration | Controlled by `access_token_expires()`    |
| Claims     | `sub` (user ID), `username`, `iat`, `exp` |

Example decoded JWT payload:

```json
{
  "sub": "1",
  "username": "user1",
  "iat": 1731164400,
  "exp": 1731168000
}
```

---

## Role-Based Access Control (RBAC)

Role validation is implemented using the dependency function:

```python
from app.utils.auth_deps import require_roles

@router.get("/admin/ping")
async def admin_ping(_: User = Depends(require_roles("admin"))):
    return {"ok": True}
```

If the user does not have the required role, the server returns:

```json
{"detail": "Insufficient role"}
```

---

## API Endpoints

### `POST /api/register`

Registers a new user.

* Hashes password using bcrypt.
* Default role: `user`.
* Checks username and email uniqueness.

**Example request:**

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","email":"user1@example.com","password":"SuperHaslo123"}'
```

**Response:**

```json
{"message": "User created successfully"}
```

---

### `POST /api/login`

Authenticates user credentials and returns a JWT token.

**Example request:**

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"SuperHaslo123"}'
```

**Response:**

```json
{
  "token": "JWT_TOKEN",
  "user": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com",
    "role": "user"
  }
}
```

---

### `GET /api/me`

Returns information about the currently authenticated user.
Requires the header:
`Authorization: Bearer <JWT_TOKEN>`

**Example:**

```bash
curl http://localhost:8000/api/me \
  -H "Authorization: Bearer JWT_TOKEN"
```

**Response:**

```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com",
  "role": "user"
}
```

---

### `POST /api/logout`

Performs logical logout (client-side).
No server blacklist is maintained.

**Example:**

```bash
curl -X POST http://localhost:8000/api/logout \
  -H "Authorization: Bearer JWT_TOKEN"
```

**Response:** HTTP `204 No Content`

---

---

## Summary

| Component        | Description                                    |
| ---------------- | ---------------------------------------------- |
| Framework        | FastAPI                                        |
| ORM              | SQLAlchemy (Async)                             |
| Auth             | JWT (HTTP Bearer)                              |
| Password Hashing | bcrypt                                         |
| Roles            | `user`, `admin`                                |
| API Docs         | `/docs` (Swagger UI)                           |
| Database         | SQLite (dev), compatible with PostgreSQL/MySQL |

