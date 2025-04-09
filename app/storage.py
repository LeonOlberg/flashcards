from minio import Minio
from flask import current_app
import os
from datetime import timedelta
import magic

class StorageService:
    def __init__(self):
        self.client = Minio(
            "localhost:9000",
            access_key="minioadmin",
            secret_key="minioadmin",
            secure=False
        )
        self.bucket_name = "flash-cards"
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload_file(self, file, card_id, side):
        """Upload a file to MinIO and return the object path."""
        if not file:
            return None

        # Generate a unique filename
        file_extension = os.path.splitext(file.filename)[1]
        object_name = f"{card_id}/{side}{file_extension}"

        # Get file size and content type
        file_size = os.fstat(file.fileno()).st_size
        content_type = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)  # Reset file pointer

        # Upload the file
        self.client.put_object(
            self.bucket_name,
            object_name,
            file,
            file_size,
            content_type=content_type
        )

        return object_name

    def get_file_url(self, object_name):
        """Generate a presigned URL for the object."""
        if not object_name:
            return None
        try:
            return self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=timedelta(days=7)
            )
        except Exception as e:
            current_app.logger.error(f"Error generating presigned URL: {str(e)}")
            return None

storage_service = StorageService()
