# app/schemas/file.py
from pydantic import BaseModel

class FileUploadResponse(BaseModel):
    uri: str