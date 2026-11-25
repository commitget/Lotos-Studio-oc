import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db, SessionLocal
from app.core.middleware import setup_middleware, limiter
from app.core.models import User, UserRole
from app.core.security import hash_password, generate_salt
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    _seed_admin()
    yield


def _seed_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin:
            salt = generate_salt()
            hashed = hash_password("Admin123!", salt)
            admin = User(
                email=settings.ADMIN_EMAIL,
                username="admin",
                hashed_password=hashed,
                salt=salt,
                role=UserRole.SUPER_ADMIN,
                is_verified=True,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

setup_middleware(app)
app.include_router(api_router)


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": type(exc).__name__},
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
