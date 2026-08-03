from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import shutil
import os

from app.database.database import get_db
from app.models.file import File as FileModel
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    os.makedirs("uploads", exist_ok=True)   
    filepath = os.path.join("uploads", file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_file = FileModel(
        filename=file.filename,
        owner_id=current_user.id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }