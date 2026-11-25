from fastapi import APIRouter
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.marketplace.router import router as marketplace_router
from app.modules.betatesting.router import router as betatesting_router
from app.modules.billing.router import router as billing_router
from app.modules.crm.router import router as crm_router
from app.modules.notifications.router import router as notifications_router
from app.modules.admin.router import router as admin_router
from app.modules.support.router import router as support_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(marketplace_router, prefix="/marketplace", tags=["marketplace"])
api_router.include_router(betatesting_router, prefix="/beta", tags=["beta"])
api_router.include_router(billing_router, prefix="/billing", tags=["billing"])
api_router.include_router(crm_router, prefix="/crm", tags=["crm"])
api_router.include_router(notifications_router, prefix="/notifications", tags=["notifications"])
api_router.include_router(support_router, prefix="/support", tags=["support"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
