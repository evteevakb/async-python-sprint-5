"""Application tests"""
from httpx import AsyncClient
from fastapi import status
import pytest

from main import app


TEST_USERNAME = 'test_username'
TEST_PASSWORD = 'test_password'


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
    @pytest.mark.dependency(depends=["TestService::test_ping"])
    async def test_user_registration(self, client: AsyncClient) -> None:
        """Tests POST /register endpoint"""
        response = await client.post(app.url_path_for('register_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        assert response.status_code == status.HTTP_201_CREATED
        response = await client.post(app.url_path_for('register_user'),
                                     json={'username': TEST_USERNAME, 'password': TEST_PASSWORD})
        assert response.status_code == status.HTTP_403_FORBIDDEN
