# app/api/v1/endpoints/file.py
import uuid
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header, status
from minio import Minio

from app.core.storage import get_minio_client, build_public_uri
from app.core.config import settings
from app.schemas.file import FileUploadResponse

router = APIRouter()
MAX_SIZE = 100 * 1024  # 100 KiB
ALLOWED_CT = {"image/jpeg", "image/jpg", "image/png"}

# --- sementara: cek ada header Bearer ---
def require_bearer(auth: Annotated[str | None, Header(alias="Authorization")] = None):
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return True

@router.post("/file", response_model=FileUploadResponse, status_code=200, tags=["file"])
async def upload_file(
    _ok: bool = Depends(require_bearer),  # nanti bisa diganti ke deps.get_current_user
    file: UploadFile = File(...),
    client: Minio = Depends(get_minio_client),
):
    # Validasi content-type
    ct = (file.content_type or "").lower()
    if ct not in ALLOWED_CT:
        raise HTTPException(status_code=400, detail="file must be jpeg/jpg/png")

    # Baca isi file
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="file size exceeds 100KiB")

    # Tentukan ekstensi
    ext = ".jpg" if "jpeg" in ct or "jpg" in ct else ".png"
    object_name = f"{uuid.uuid4().hex}{ext}"

    # Upload ke MinIO
    client.put_object(
        bucket_name=settings.MINIO_BUCKET,
        object_name=object_name,
        data=BytesIO(content),
        length=len(content),
        content_type=ct,
    )

    # Bangun URL publik
    return FileUploadResponse(uri=build_public_uri(object_name))