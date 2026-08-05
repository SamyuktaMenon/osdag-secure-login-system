from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import shutil
import os

from app.database.database import get_db
from app.models.file import File as FileModel
from app.models.user import User
from app.utils.auth import get_current_user
from app.schemas.file import FileResponse as FileSchema

router = APIRouter()


# ---------------- UPLOAD ----------------
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


# ---------------- LIST FILES ----------------
@router.get("/files", response_model=list[FileSchema])
def get_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    files = (
        db.query(FileModel)
        .filter(FileModel.owner_id == current_user.id)
        .all()
    )

    return files


# ---------------- DOWNLOAD ----------------
@router.get("/download/{file_id}")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file = (
        db.query(FileModel)
        .filter(
            FileModel.id == file_id,
            FileModel.owner_id == current_user.id
        )
        .first()
    )

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    filepath = os.path.join("uploads", file.filename)

    return FileResponse(
        path=filepath,
        filename=file.filename
    )


# ---------------- DELETE ----------------
@router.delete("/delete/{file_id}")
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file = (
        db.query(FileModel)
        .filter(
            FileModel.id == file_id,
            FileModel.owner_id == current_user.id
        )
        .first()
    )

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    filepath = os.path.join("uploads", file.filename)

    if os.path.exists(filepath):
        os.remove(filepath)

    db.delete(file)
    db.commit()

    return {
        "message": "File deleted successfully"
    }