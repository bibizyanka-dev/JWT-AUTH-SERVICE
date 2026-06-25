
import bcrypt
from fastapi import Depends, HTTPException, status
from src.schemas.user import UserRead
from src.repositories.user import UserRepository
from src.utils.logging import log_service
import logging
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

class UserService:

    @staticmethod
    @log_service(logger=logger, log_result=True)
    async def get_user_by_id_or_none(db: AsyncSession, user_id: int) -> UserRead | None:
        user = await UserRepository.select_user(db, user_id)
        if user is None:
            return None
        return UserRead.model_validate(user)
    
    @staticmethod
    @log_service(logger=logger, log_result=True)
    async def get_user_by_id(db: AsyncSession, user_id: int) -> UserRead:
        user = await UserService.get_user_by_id_or_none(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user