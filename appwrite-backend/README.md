<div align="center">

# ☁️ Appwrite Secure Login System

### Secure Authentication & File Management using Appwrite + FastAPI

Registration • Login • Logout • Appwrite Storage • Appwrite Database

</div>

---

# 📖 About

This implementation uses **Appwrite** as the backend service for authentication, database management, and file storage.

FastAPI acts as the REST API layer while Appwrite handles user authentication, sessions, secure storage, and database operations.

---

# ✨ Features

## Authentication

- User Registration
- User Login
- User Logout
- User Profile (/me)

## File Management

- Upload Files
- List User Files
- View Single File
- Delete File

## Security

- Password hashing handled by Appwrite
- Session-based authentication
- User isolation
- Protected API routes

---

# 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI |
| Backend Service | Appwrite |
| Storage | Appwrite Storage |
| Database | Appwrite Database |
| Authentication | Appwrite Sessions |

---

# 🚀 Setup

## Install

```bash
pip install -r requirements.txt
```

Run

```bash
uvicorn app.main:app --reload
```

Open

```
http://127.0.0.1:8000/docs
```

---

# Authentication

This implementation uses **Appwrite Session Authentication**.

Unlike JWT, Appwrite securely manages sessions and validates them automatically.

---

# Logout

Logout is implemented by deleting the current Appwrite session.

Once the session is removed, authenticated requests immediately become unauthorized.

---

# User Isolation

Each uploaded file stores the owner's Appwrite user ID.

Every protected endpoint verifies ownership before returning or deleting a file.

A user cannot access another user's files even if they know the file ID.

---

# What Appwrite Handles Automatically

- User Authentication
- Password Hashing
- Session Management
- Storage Security
- User Management

---

# What Was Configured

- Storage Bucket
- Database
- Collections
- File Metadata
- FastAPI Routes
- Ownership Verification

---

# Future Improvements

- Refresh Tokens
- File Type Validation
- Role-Based Access Control
- Docker Support
- CI/CD