from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.services.appwrite_client import users, account
from appwrite.id import ID

router = APIRouter()


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str    

class LogoutRequest(BaseModel):
    userId: str
    sessionId: str   


@router.post("/register")
def register(data: RegisterRequest):

    try:
        user = users.create(
            user_id=ID.unique(),
            email=data.email,
            password=data.password,
            name=data.name
        )

        return {
            "message": "User registered successfully",
            "userId": user.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(data: LoginRequest):
    try:
        session = account.create_email_password_session(
            email=data.email,
            password=data.password
        )

    

        return {
            "message": "Login successful",
            "sessionId": session.id,
            "userId": session.userid,
            "secret": session.secret
        }

    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=str(e)
        )

@router.post("/logout")
def logout(data: LogoutRequest):
    try:
        users.delete_session(
            user_id=data.userId,
            session_id=data.sessionId
        )

        return {
            "message": "Logged out successfully"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/me/{user_id}")
def get_me(user_id: str):
    try:
        user = users.get(user_id)

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )    