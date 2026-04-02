from fastapi import APIRouter
from src.api.auth import auth_router
# from src.api.auth import auth_router

api_router = APIRouter()

api_router.include_router(auth_router)