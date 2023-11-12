"""Application tests"""
from httpx import AsyncClient
from fastapi import status
import pytest

from main import app


TEST_USERNAME = 'test_username'
TEST_PASSWORD = 'test_password'
TEST_INCORRECT_USERNAME = 'incorrect_username'
TEST_INCORRECT_PASSWORD = 'incorrect_password'
TEST_INCORRECT_TOKEN = 'test_token'
TEST_FILE = 'tests/test_file.txt'
TEST_DOWNLOADED_FILEPATH = 'tests/test_file_output.txt'
TEST_INCORRECT_FILEPATH = 'test_incorrect_filepath'

pytestmark = pytest.mark.asyncio


class TestService:
    """Tests for checking endpoints in 'service' tag"""
    @pytest.mark.dependency()
    async def test_ping(self, client: AsyncClient) -> None:
        """Tests GET /ping endpoint"""
        response = await client.get(app.url_path_for('ping'))
        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        assert response['db'] >= 0. and response['storage'] >= 0.


class TestUser:
    """Tests for checking endpoints in 'user' tag"""
    @pytest.mark.dependency()
    @pytest.mark.dependency(depends=["TestService::test_ping"])
    async def test_user_registration(self, client: AsyncClient) -> None:
        """Tests POST /register endpoint"""
        response = await client.post(app.url_path_for('register_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        assert response.status_code == status.HTTP_201_CREATED
        response = await client.post(app.url_path_for('register_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

    @pytest.mark.dependency(depends=["TestUser::test_user_registration"])
    async def test_user_authentication(self, client: AsyncClient) -> None:
        """Tests POST /auth endpoint with correct data"""
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        assert response.status_code == status.HTTP_200_OK
        first_token = response.json()['token']
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        assert response.status_code == status.HTTP_200_OK
        assert first_token == response.json()['token']

    @pytest.mark.dependency(depends=["TestUser::test_user_registration"])
    async def test_user_authentication_incorrect_username(self, client: AsyncClient) -> None:
        """Tests POST /auth endpoint with incorrect username"""
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_INCORRECT_USERNAME,
                                           'password': TEST_PASSWORD})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.dependency(depends=["TestUser::test_user_registration"])
    async def test_user_authentication_incorrect_password(self, client: AsyncClient) -> None:
        """Tests POST /auth endpoint with incorrect password"""
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_USERNAME,
                                           'password': TEST_INCORRECT_PASSWORD})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestFiles:
    """Tests for checking endpoints in 'file_storage' tag"""
    @pytest.mark.dependency()
    @pytest.mark.dependency(depends=["TestService::test_ping"])
    async def test_files_authentication_required(self, client: AsyncClient) -> None:
        """Tests GET /files for authentication requirement"""
        response = await client.get(app.url_path_for('get_files'),
                                    params={'token': TEST_INCORRECT_TOKEN})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.dependency(depends=["TestFiles::test_files_authentication_required"])
    async def test_files_empty_list(self, client: AsyncClient) -> None:
        """Tests GET /files with empty list of files"""
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        token = response.json()['token']
        response = await client.get(app.url_path_for('get_files'), params={'token': token})
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    @pytest.mark.dependency()
    @pytest.mark.dependency(depends=["TestService::test_ping"])
    async def test_upload_authentication_required(self, client: AsyncClient) -> None:
        """Tests POST /files/upload for authentication requirement"""
        response = await client.post(app.url_path_for('upload_file'),
                                     params={'token': TEST_INCORRECT_TOKEN},
                                     files={'uploadFile': open(TEST_FILE, 'rb')})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.dependency()
    @pytest.mark.dependency(depends=["TestFiles::test_upload_authentication_required"])
    async def test_upload(self, client: AsyncClient) -> None:
        """Tests POST /files/upload"""
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        token = response.json()['token']
        with open(TEST_FILE, 'rb') as test_file:
            response = await client.post(app.url_path_for('upload_file'),
                                         params={'token': token},
                                         files={'file': ('test_file', test_file, 'plain/text')})
        assert response.status_code == status.HTTP_201_CREATED
        with open(TEST_FILE, 'rb') as test_file:
            response = await client.post(app.url_path_for('upload_file'),
                                         params={'token': token},
                                         files={'file': ('test_file', test_file, 'plain/text')})
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

    async def test_files(self, client: AsyncClient) -> None:
        """Tests GET /files with previously uploaded files"""
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        token = response.json()['token']
        response = await client.get(app.url_path_for('get_files'), params={'token': token})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) > 0

    async def test_download_without_parameters(self, client: AsyncClient) -> None:
        """Tests GET /files/download without passing any parameters"""
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        token = response.json()['token']
        response = await client.get(app.url_path_for('download_file'),
                                    params={'token': token})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_download_nonexistent_file(self, client: AsyncClient) -> None:
        """Tests GET /files/download with nonexistent filepath"""
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        token = response.json()['token']
        response = await client.get(app.url_path_for('download_file'),
                                    params={'token': token, 'filepath': TEST_INCORRECT_FILEPATH})
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_download(self, client: AsyncClient) -> None:
        """Tests GET /files/download"""
        response = await client.post(app.url_path_for('authenticate_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        token = response.json()['token']
        response = await client.get(app.url_path_for('get_files'), params={'token': token})
        filepath = response.json()[0]['filepath']
        response = await client.get(app.url_path_for('download_file'),
                                    params={'token': token, 'filepath': filepath})
        with open(TEST_DOWNLOADED_FILEPATH, 'wb') as test_file:
            test_file.write(response.content)
