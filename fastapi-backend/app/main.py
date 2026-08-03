from fastapi import FastAPI

from app.database.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.files import router as file_router

import app.models.user
import app.models.file

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(file_router)


@app.get("/")
def root():
    return {
        "message": "Secure Login System API Running"
    }