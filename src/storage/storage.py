import os

from miniopy_async import Minio
from miniopy_async.error import MinioException


MINIO_BUCKET = os.environ['MINIO_BUCKET_NAME']
MINIO_PORT = os.environ['MINIO_PORT']
MINIO_ROOT_USER = os.environ['MINIO_ROOT_USER']
MINIO_ROOT_PASSWORD = os.environ['MINIO_ROOT_PASSWORD']


class MinioClient:
    def __init__(self) -> None:
        self.minio = Minio(f'minio:{MINIO_PORT}', access_key=MINIO_ROOT_USER,
                           secret_key=MINIO_ROOT_PASSWORD, secure=False)
        self.bucket = MINIO_BUCKET

    async def check_bucket(self) -> None:
        result = await self.minio.bucket_exists(self.bucket)
        if not result:
            raise MinioException(f'Bucket {self.bucket} does not exist')
