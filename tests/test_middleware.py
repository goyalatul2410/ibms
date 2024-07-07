
import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.testclient import TestClient
from unittest.mock import patch
from app.middleware.auth_middleware import AuthMiddleware
import os

API_KEY = '1234567890abcdef'
os.environ['API_KEY'] = API_KEY


def create_app():
    app = FastAPI()

    app.add_middleware(AuthMiddleware)

    @app.get("/protected")
    async def protected():
        return {"message": "Protected route"}

    return app


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as client:
        yield client


def test_auth_middleware_missing_header(client):
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json() == "Authorization header missing"


def test_auth_middleware_invalid_key(client):
    headers = {"Authorization": "Bearer invalidapikey"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert response.json() == "Invalid or missing API key"


def test_auth_middleware_valid_key(client):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = client.get("/protected", headers=headers)
    print(response.status_code, "-------------")
    assert response.status_code == 200
    assert response.json() == {"message": "Protected route"}
