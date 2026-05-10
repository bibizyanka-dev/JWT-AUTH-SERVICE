from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import async_session
from fastapi_jwt import JwtAuthorizationCredentials
from src.utils.security import access_security
from src.schemas.auth import UserRead
from src.services.user import UserService
from fastapi import Depends, HTTPException

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_current_user(db: AsyncSession = Depends(get_db), credentials: JwtAuthorizationCredentials = Depends(access_security)) -> UserRead:
    token_type = credentials.subject.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user_id = credentials.subject.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user = await UserService.get_user_by_id_or_none(db, user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    return UserRead.model_validate(user)