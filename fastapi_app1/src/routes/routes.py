from fastapi import APIRouter

from src.api.v1.UserAuthentication.views import auth_views

# Add route with prefix /api/v1 to manage v1 APIs.
router = APIRouter(prefix="/api/v1/auth-views")
router.include_router(auth_views.app1, tags=["App1 User Authentication Views"])