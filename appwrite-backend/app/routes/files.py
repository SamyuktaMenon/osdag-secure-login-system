from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.services.appwrite_client import storage, databases
from app.config import settings
from appwrite.id import ID
from appwrite.input_file import InputFile
from fastapi import HTTPException
from appwrite.query import Query
import os

router = APIRouter()


@router.post("/upload")
async def upload_file(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Save temporarily
        temp_path = file.filename

        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # Upload to Appwrite Storage
        uploaded = storage.create_file(
            bucket_id=settings.BUCKET_ID,
            file_id=ID.unique(),
            file=InputFile.from_path(temp_path)
        )

        # Delete temporary file
        os.remove(temp_path)

        # Generate download URL
        download_url = (
            f"{settings.APPWRITE_ENDPOINT}/storage/buckets/"
            f"{settings.BUCKET_ID}/files/{uploaded.id}/view"
        )

        # Save metadata in Appwrite Database
        databases.create_document(
            database_id=settings.DATABASE_ID,
            collection_id=settings.FILES_COLLECTION_ID,
            document_id=ID.unique(),
            data={
                "fileName": file.filename,
                "fileId": uploaded.id,
                "userId": user_id,
                "downloadUrl": download_url
            }
        )

        return {
            "message": "File uploaded successfully",
            "fileId": uploaded.id,
            "downloadUrl": download_url
        }

    except Exception as e:
        # Remove temp file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/")
def list_files(user_id: str):
    try:
        result = databases.list_documents(
            database_id=settings.DATABASE_ID,
            collection_id=settings.FILES_COLLECTION_ID,
            queries=[
                Query.equal("userId", user_id)
            ]
        )

        return {
            "count": result.total,
            "files": result.documents
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.delete("/{file_id}")
def delete_file(file_id: str):
    try:
        # Find the document corresponding to this file
        result = databases.list_documents(
            database_id=settings.DATABASE_ID,
            collection_id=settings.FILES_COLLECTION_ID,
            queries=[
                Query.equal("fileId", file_id)
            ]
        )

        if result.total == 0:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        document = result.documents[0]

        # Delete file from Storage
        storage.delete_file(
            bucket_id=settings.BUCKET_ID,
            file_id=file_id
        )

        # Delete metadata from Database
        databases.delete_document(
            database_id=settings.DATABASE_ID,
            collection_id=settings.FILES_COLLECTION_ID,
            document_id=document.id
        )

        return {
            "message": "File deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )    


@router.get("/{file_id}")
def get_file(file_id: str, user_id: str):
    try:
        result = databases.list_documents(
            database_id=settings.DATABASE_ID,
            collection_id=settings.FILES_COLLECTION_ID,
            queries=[
                Query.equal("fileId", file_id)
            ]
        )

        if result.total == 0:
            raise HTTPException(
                status_code=404,
                detail="File not found"
            )

        document = result.documents[0]

        # User isolation
        if document.data["userId"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return {
            "fileName": document.data["fileName"],
            "fileId": document.data["fileId"],
            "downloadUrl": document.data["downloadUrl"]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )   