
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.types import ASGIApp
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
            return await call_next(request)

        if 'Authorization' not in request.headers:
            return JSONResponse(status_code=401, content="Authorization header missing")

        auth_header = request.headers['Authorization']
        if auth_header != f"Bearer {API_KEY}":
            return JSONResponse(status_code=401, content="Invalid or missing API key")

        response = await call_next(request)
        return response
