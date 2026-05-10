from fastapi import APIRouter, Depends
from src.schemas.auth import UserRead
from src.utils.dependencies import get_current_user

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/me", response_model=UserRead)
async def me(user: UserRead = Depends(get_current_user)):
    return UserRead.model_validate(user)