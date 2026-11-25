from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.auth import (
    RegisterRequest, LoginRequest, TokenResponse, RefreshRequest,
    Verify2FARequest, Enable2FAResponse, UserResponse
)
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.core.models import User

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        user = service.register(request.email, request.username, request.password)
        tokens = service.create_tokens(user)
        service.save_session(user.id, tokens["refresh_token"])
        return TokenResponse(**tokens)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, req: Request, db: Session = Depends(get_db)):
    service = AuthService(db)
    user = service.authenticate(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.totp_enabled:
        raise HTTPException(status_code=403, detail="2FA required")

    tokens = service.create_tokens(user)
    service.save_session(user.id, tokens["refresh_token"], req.client.host, req.headers.get("user-agent"))
    return TokenResponse(**tokens)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    tokens = service.refresh_tokens(request.refresh_token)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    return TokenResponse(**tokens)


@router.post("/2fa/enable", response_model=Enable2FAResponse)
async def enable_2fa(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = AuthService(db)
    result = service.enable_2fa(current_user)
    return Enable2FAResponse(**result)


@router.post("/2fa/verify")
async def verify_2fa(request: Verify2FARequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    service = AuthService(db)
    if service.verify_2fa(current_user, request.code):
        current_user.totp_enabled = True
        db.commit()
        return {"detail": "2FA enabled successfully"}
    raise HTTPException(status_code=400, detail="Invalid code")


@router.post("/2fa/authenticate", response_model=TokenResponse)
async def authenticate_2fa(request: Verify2FARequest, req: Request, db: Session = Depends(get_db)):
    email = req.headers.get("X-2FA-Email")
    if not email:
        raise HTTPException(status_code=400, detail="Email header required")
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.totp_enabled:
        raise HTTPException(status_code=400, detail="2FA not configured")
    service = AuthService(db)
    if service.verify_2fa(user, request.code):
        tokens = service.create_tokens(user)
        return TokenResponse(**tokens)
    raise HTTPException(status_code=400, detail="Invalid 2FA code")


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sessions = db.query(User).filter(User.id == current_user.id).first()
    if sessions:
        for s in db.query(type(current_user)).filter(type(current_user).id == current_user.id):
            pass
    return {"detail": "Logged out"}
