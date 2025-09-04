# app/core/storage.py
from minio import Minio
from app.core.config import settings

def get_minio_client() -> Minio:
    """
    Create and return a MinIO client.
    Ensures the connection uses the settings from config.
    """
    client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE,
        region=settings.MINIO_REGION,
    )
    # Pastikan bucket ada, kalau belum buat
    if not client.bucket_exists(settings.MINIO_BUCKET):
        client.make_bucket(settings.MINIO_BUCKET, location=settings.MINIO_REGION)
    return client

def build_public_uri(object_name: str) -> str:
    """
    Build a public URI for an object in the bucket.
    """
    scheme = "https" if settings.MINIO_SECURE else "http"
    return f"{scheme}://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET}/{object_name}"