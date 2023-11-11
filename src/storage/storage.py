import os

from minio import Minio
from minio.error import MinioException


MINIO_BUCKET = os.environ['MINIO_BUCKET_NAME']
MINIO_PORT = os.environ['MINIO_PORT']
MINIO_ROOT_USER = os.environ['MINIO_ROOT_USER']
MINIO_ROOT_PASSWORD = os.environ['MINIO_ROOT_PASSWORD']


class MinioClient:
    def __init__(self) -> None:
        self.minio = Minio(f'minio:{MINIO_PORT}', access_key=MINIO_ROOT_USER,
                           secret_key=MINIO_ROOT_PASSWORD, secure=False)
        self.bucket = MINIO_BUCKET
        if not self.minio.bucket_exists(self.bucket):
            raise MinioException(f'Bucket {self.bucket} does not exist')
