from pydantic import BaseModel

class FileResponse(BaseModel):
    id: int
    filename: str

    class Config:
        from_attributes = True