# 🔐 OSDAG Secure Login System

This repository contains two independent implementations of the same secure authentication and file management system.

## Repository Structure

```
osdag-secure-login-system
│
├── frontend/
├── fastapi-backend/
└── appwrite-backend/
```

## Implementations

### 🐍 FastAPI Backend

Features

- JWT Authentication
- Password Hashing
- File Upload
- File Download
- User Profile
- Protected APIs
- Rate Limiting
- SQLite/PostgreSQL

📄 Documentation

➡️ [FastAPI Backend Documentation](fastapi-backend/README.md)

---

### ☁️ Appwrite Backend

Features

- Appwrite Authentication
- Appwrite Database
- Appwrite Storage
- User Sessions

📄 Documentation

➡️ [Appwrite Backend Documentation](appwrite-backend/README.md)

---

## Frontend

The provided frontend is shared between both implementations.

```
frontend/
```

---

---

# Assignment Notes

## JWT vs Session Authentication

The FastAPI implementation uses JWT authentication because it is stateless, scalable, and well suited for REST APIs.

The Appwrite implementation uses session-based authentication because Appwrite securely manages user sessions, authentication, and session invalidation automatically.

---

## Logout

FastAPI invalidates JWTs using a server-side blacklist.

Appwrite logs users out by deleting their active session.

---

## User Isolation

Every protected endpoint validates the authenticated user before accessing data.

Files are associated with their owner's user ID.

A request for another user's file returns an authorization error even if the file exists.

---

## Appwrite Responsibilities

Appwrite automatically provides:

- Password hashing
- User authentication
- Session management
- Storage
- Database permissions

The application configures:

- Storage buckets
- Database collections
- Ownership verification
- API routes

---

## Future Improvements

- Refresh Tokens
- Docker
- PostgreSQL
- CI/CD
- Email Verification
- RBAC

## Author

Samyukta Menon
