from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.person import router as person_router
from app.api.v1.user import router as user_router
from app.api.v1.profile import router as profile_router
from app.api.v1.role import router as role_router
from app.api.v1.permission import router as permission_router
from app.api.v1.role_permission import router as role_permission_router
from app.api.v1.user_role import router as user_role_router
from app.api.v1.theme import router as theme_router
from app.api.v1.organization_setting import router as organization_setting_router
from app.api.v1.notification import router as notification_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(person_router)
api_router.include_router(user_router)
api_router.include_router(profile_router)
api_router.include_router(role_router)
api_router.include_router(permission_router)
api_router.include_router(role_permission_router)
api_router.include_router(user_role_router)
api_router.include_router(notification_router)
api_router.include_router(theme_router)
api_router.include_router(organization_setting_router)
