from fastapi import APIRouter
from .anime_router import router as anime_router
from .user_router import router as user_router
from .start_router import router as start_router
from .review_router import router as review_router
from .jwt_auth_router import router as jwt_auth_router
from .al_bd_router import router as al_bd_router

all_routers = [al_bd_router, jwt_auth_router, user_router, anime_router, review_router, start_router]