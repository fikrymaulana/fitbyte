# app/api/v1/endpoints/file.py
import uuid
from io import BytesIO
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status # <-- Tambahkan status

from minio import Minio

from app.core.storage import get_minio_client, build_public_uri
from app.core.config import settings
from app.schemas.file import FileUploadResponse
from app.api.deps import get_current_user
from app.models.auth import Authentication  # <-- PERUBAHAN 1: Impor model user Anda

router = APIRouter()
MAX_SIZE = 100 * 1024  # 100 KiB
ALLOWED_CT = {"image/jpeg", "image/jpg", "image/png"}

# PERUBAHAN 2: Ubah status code menjadi 201
@router.post("/file", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    # PERUBAHAN 3: Tambahkan type hint untuk autocomplete yang lebih baik
    current_user: Authentication = Depends(get_current_user),
    file: UploadFile = File(...),
    client: Minio = Depends(get_minio_client),
):
    """
    Mengunggah file gambar (jpg/png) dengan ukuran maks 100KB.
    Memerlukan otentikasi JWT yang valid.
    """
    ct = (file.content_type or "").lower()
    if ct not in ALLOWED_CT:
        raise HTTPException(status_code=400, detail="Tipe file harus jpeg/jpg/png")

    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="Ukuran file melebihi 100KB")

    ext = ".jpg" if "jpeg" in ct or "jpg" in ct else ".png"
    
    # PERUBAHAN 4: Manfaatkan user ID untuk membuat path yang terorganisir
    object_name = f"user_{current_user.id}/{uuid.uuid4().hex}{ext}"

    try:
        client.put_object(
            bucket_name=settings.MINIO_BUCKET,
            object_name=object_name,
            data=BytesIO(content),
            length=len(content),
            content_type=ct,
        )
    except Exception as e:
        # Menambahkan penanganan error jika upload MinIO gagal
        raise HTTPException(status_code=503, detail=f"Tidak dapat mengunggah file: {e}")
        
    return FileUploadResponse(uri=build_public_uri(object_name))

