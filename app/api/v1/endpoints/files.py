import uuid
import io
from typing import Annotated, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.minio_client import MinIOClient
from app.api.deps import get_current_user_payload

router = APIRouter()

# Security scheme for Bearer token
bearer = HTTPBearer(auto_error=False)

ALLOWED_EXTENSIONS = {"jpeg", "jpg", "png"}
MAX_FILE_SIZE = 100 * 1024  # 100 KiB

def get_current_user(creds: HTTPAuthorizationCredentials) -> dict:
    if not creds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_header = f"Bearer {creds.credentials}"

    return get_current_user_payload(auth_header)

@router.post("/file")
async def upload_file(
    file: Optional[UploadFile] = File(None),
    creds: HTTPAuthorizationCredentials = Depends(bearer)
) -> dict:
  """
  Upload a file to MinIO storage.

  - File must be JPEG, JPG, or PNG format
  - Maximum file size is 100 KiB
  """

  # Validate Bearer token first
  current_user = get_current_user(creds)

  # Validate file if provided
  if not file:
    raise HTTPException(
        status_code=400,
        detail="File is required"
    )

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