from fastapi import APIRouter
from .auth_router import router as auth_router
from .anime_router import router as anime_router
from .user_router import router as user_router
from .start_router import router as start_router

router = APIRouter()

router.include_router(auth_router)

all_routers = [
    start_router,
    auth_router,
    anime_router,
    user_router
]