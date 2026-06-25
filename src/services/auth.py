import logging
import bcrypt
from fastapi import HTTPException
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.auth import AuthRepository
from src.repositories.user import UserRepository
from src.schemas.user import UserRead
from src.utils.logging import log_service
from src.utils.security import access_security, refresh_security
from src.schemas.auth import RegistrationRequest, LoginRequest, RefreshResponse, AuthTokens

logger = logging.getLogger(__name__)

class AuthService:

    @staticmethod
    @log_service(logger=logger, log_result=True)
    async def refresh(db: AsyncSession, credentials: JwtAuthorizationCredentials) -> RefreshResponse:
        payload = credentials.subject

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await UserRepository.select_user(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        new_access_token = access_security.create_access_token(
            subject={
                "sub": str(user.id),
                "username": user.username,
                "type": "access"
            }
        )

        new_refresh_token = refresh_security.create_refresh_token(
            subject={
                "sub": str(user.id),
                "username": user.username,
                "type": "refresh"
            }
        )

        return RefreshResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )

    @staticmethod
    @log_service(logger=logger, log_result=True)
    async def login(db: AsyncSession, data: LoginRequest) -> AuthTokens:
        user = await AuthRepository._get_by_email(db, data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
    
        is_valid_password = bcrypt.checkpw(
            data.password.encode("utf-8"),
            user.password.encode("utf-8")
        )

        if not is_valid_password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        user_read = UserRead.model_validate(user)

        access_token = access_security.create_access_token(
            subject={
                "sub": str(user_read.id),
                "username": user_read.username,
                "type": "access"
            }
        )

        refresh_token = refresh_security.create_refresh_token(
            subject={
                "sub": str(user_read.id),
                "username": user_read.username,
                "type": "refresh"
            }
        )

        return AuthTokens(
            user=user_read,
            access_token=access_token,
            refresh_token=refresh_token,
        )


    @staticmethod
    @log_service(logger=logger, log_result=True)
    async def registration(db: AsyncSession, data: RegistrationRequest) -> AuthTokens:
        if await AuthRepository._get_by_username(db, data.username):
            raise HTTPException(status_code=409, detail="User already exists")
        
        hashed_password = bcrypt.hashpw(
            data.password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")
        
        new_user = await AuthRepository.create_new_user(db, data.username, hashed_password, data.email)

        if not new_user:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        new_user = UserRead.model_validate(new_user)

        access_token = access_security.create_access_token(
            subject={
                "sub": str(new_user.id),
                "username": new_user.username,
                "type": "access"
            }
        )

        refresh_token = refresh_security.create_refresh_token(
            subject={
                "sub": str(new_user.id),
                "username": new_user.username,
                "type": "refresh"
            }
        )

        return AuthTokens(
            user=new_user,
            access_token=access_token,
            refresh_token=refresh_token,
        )

