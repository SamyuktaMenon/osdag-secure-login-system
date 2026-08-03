from fastapi import FastAPI

from app.database.database import Base, engine
from app.routers.auth import router as auth_router

import app.models.user
import app.models.file

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Secure Login System API Running"
    }