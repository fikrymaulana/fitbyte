from minio import Minio
from minio.error import S3Error
from app.core.config import settings

class MinIOClient:
    def __init__(self):
        self.client = Minio(
            endpoint=f"{settings.MINIO_ENDPOINT}:{settings.MINIO_PORT}",
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        self.bucket_name = settings.MINIO_BUCKET

    def _ensure_bucket_exists(self):
        """Create bucket if it doesn't exist"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' created successfully")
            else:
                print(f"Bucket '{self.bucket_name}' already exists")
        except S3Error as e:
            print(f"Error creating bucket: {e}")
            raise Exception(f"Failed to ensure bucket exists: {str(e)}")

    def upload_file(self, file_data, file_name: str, content_type: str, file_length: int) -> str:
        """Upload file to MinIO and return the file URL"""
        try:
            print(f"Starting upload for file: {file_name}")
            # Ensure bucket exists
            self._ensure_bucket_exists()

            print(f"Uploading file {file_name} to bucket {self.bucket_name}")
            # Upload the file
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=file_name,
                data=file_data,
                length=file_length,
                content_type=content_type
            )

            print(f"Upload successful for {file_name}")
            # Return the file URL
            endpoint_url = f"http://{settings.MINIO_ENDPOINT}:{settings.MINIO_PORT}"
            file_url = f"{endpoint_url}/{self.bucket_name}/{file_name}"
            print(f"File URL: {file_url}")
            return file_url
        except S3Error as e:
            print(f"S3Error during upload: {str(e)}")
            raise Exception(f"Failed to upload file: {str(e)}")
        except Exception as e:
            print(f"General error during upload: {str(e)}")
            raise Exception(f"Failed to upload file: {str(e)}")

# Remove global instance - create when needed