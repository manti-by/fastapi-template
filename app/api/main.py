from app.api.routes import auth, root, users, utils
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(root.router, tags=["root"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
