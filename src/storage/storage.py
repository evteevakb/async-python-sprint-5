"""Contains storage client"""
from io import BytesIO
import os

import aiohttp
from miniopy_async import Minio
from miniopy_async.error import MinioException


MINIO_BUCKET = os.environ['MINIO_BUCKET_NAME']
MINIO_PORT = os.environ['MINIO_PORT']
MINIO_ROOT_USER = os.environ['MINIO_ROOT_USER']
MINIO_ROOT_PASSWORD = os.environ['MINIO_ROOT_PASSWORD']


class MinioClient:
    """MinIO storage client"""
    def __init__(self) -> None:
        self.minio = Minio(f'minio:{MINIO_PORT}', access_key=MINIO_ROOT_USER,
                           secret_key=MINIO_ROOT_PASSWORD, secure=False)
        self.bucket = MINIO_BUCKET

    async def check_bucket(self) -> None:
        """Checks if self.bucket exists.

        Raises:
            MinioException: if self.bucket does not exist.
        """
        result = await self.minio.bucket_exists(self.bucket)
        if not result:
            raise MinioException(f'Bucket {self.bucket} does not exist')

    async def upload_file(self, filepath: str, content: bytes) -> None:
        """Uploads a file into the storage.

        Args:
            filepath (str): path to the file in the storage;
            content (bytes): bytes content of the uploaded file.
        """
        content = BytesIO(content)
        await self.minio.put_object(bucket_name=self.bucket, object_name=filepath,
                                    data=content, length=content.getbuffer().nbytes)

    async def download_file(self, filepath: str) -> BytesIO:
        """Downloads a file from the storage.

        Args:
            filepath (str): path to the file in the storage.

        Returns:
            BytesIO: binary stream.
        """
        async with aiohttp.ClientSession() as session:
            response = await self.minio.get_object(bucket_name=self.bucket, object_name=filepath,
                                                   session=session)
            file = await response.read()
        return BytesIO(file)
