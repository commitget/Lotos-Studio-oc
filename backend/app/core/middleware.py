import time
import re
from typing import Callable, Awaitable

from fastapi import Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings


limiter = Limiter(key_func=get_remote_address)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' https://fonts.gstatic.com; connect-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method in ("POST", "PUT", "DELETE", "PATCH"):
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                pass
            elif "multipart/form-data" in content_type:
                pass
            elif "application/x-www-form-urlencoded" in content_type:
                form = await request.form()
                csrf_token = form.get("csrf_token")
                expected = request.headers.get("X-CSRF-Token")
                if not csrf_token or not expected or csrf_token != expected:
                    raise HTTPException(status_code=403, detail="CSRF validation failed")
        return await call_next(request)


class SQLInjectionMiddleware(BaseHTTPMiddleware):
    SQLI_PATTERNS = [
        r"(\%27)|(\')|(\-\-)|(\%23)|(#)",
        r"(\%22)|(\")",
        r"((\%27)|(\'))\s*((\%6F)|o|(\%4F))((\%72)|r|(\%52))",
        r"((\%27)|(\'))\s*((\%55)|u|(\%55))((\%6E)|n|(\%4E))((\%49)|i|(\%49))((\%4F)|o|(\%4F))((\%4E)|n|(\%4E))",
        r"\b(ALTER|CREATE|DELETE|DROP|EXEC|INSERT|MERGE|SELECT|UPDATE|UNION|TRUNCATE)\b",
        r"\b(OR|AND)\s+\d+\s*[=<>\-]",
    ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.method in ("POST", "PUT", "PATCH"):
            if "application/json" in request.headers.get("content-type", ""):
                try:
                    body = await request.json()
                    self._check_values(body)
                except Exception:
                    pass
            elif "application/x-www-form-urlencoded" in request.headers.get("content-type", ""):
                form = await request.form()
                for value in form.values():
                    if isinstance(value, str):
                        self._check_value(value)
            elif "multipart/form-data" in request.headers.get("content-type", ""):
                form = await request.form()
                for value in form.values():
                    if isinstance(value, str):
                        self._check_value(value)

        qs = str(request.query_params)
        self._check_value(qs)
        return await call_next(request)

    def _check_values(self, data, depth=0):
        if depth > 5:
            return
        if isinstance(data, dict):
            for v in data.values():
                self._check_values(v, depth + 1)
        elif isinstance(data, list):
            for v in data:
                self._check_values(v, depth + 1)
        elif isinstance(data, str):
            self._check_value(data)

    def _check_value(self, value: str):
        for pattern in self.SQLI_PATTERNS:
            if re.search(pattern, value, re.IGNORECASE):
                raise HTTPException(status_code=400, detail="Potential SQL injection detected")


def setup_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-CSRF-Token"],
    )
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(CSRFMiddleware)
    app.add_middleware(SQLInjectionMiddleware)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
