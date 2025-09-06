import uuid
import io
from typing import Annotated
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.minio_client import MinIOClient

router = APIRouter()

ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png"}
MAX_FILE_SIZE = 100 * 1024  # 100 KiB

@router.post("/file")
async def upload_file(file: Annotated[UploadFile, File(...)]) -> dict:
  """
  Upload a file to MinIO storage.

  - File must be JPEG, JPG, or PNG format
  - Maximum file size is 100 KiB
  """

  # Validate file extension
  file_extension = file.filename.split(".")[-1].lower() if "." in file.filename else ""
  if file_extension not in ALLOWED_EXTENSIONS:
    raise HTTPException(
        status_code=400,
        detail=f"Invalid file format. Allowed formats: {', '.join(ALLOWED_EXTENSIONS)}"
    )

  # Read file content
  file_content = await file.read()

  # Validate file size
  if len(file_content) > MAX_FILE_SIZE:
    raise HTTPException(
        status_code=400,
        detail=f"File too large. Maximum size: {MAX_FILE_SIZE} bytes"
    )

  # Generate unique filename
  unique_filename = f"{uuid.uuid4()}.{file_extension}"

  # Determine content type
  content_type = f"image/{file_extension}"
  if file_extension == "jpg":
    content_type = "image/jpeg"

  try:
    # Create new MinIO client instance
    minio_client = MinIOClient()

    # Create BytesIO object for MinIO
    file_stream = io.BytesIO(file_content)
    file_length = len(file_content)

    # Upload to MinIO
    file_url = minio_client.upload_file(
        file_data=file_stream,
        file_name=unique_filename,
        content_type=content_type,
        file_length=file_length
    )

    return {
        "filename": unique_filename,
        "uri": file_url,
        "size": len(file_content),
        "content_type": content_type
    }

  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")