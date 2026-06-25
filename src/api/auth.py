from fastapi import APIRouter, Depends, Security, Response
from src.utils.security import refresh_security
from fastapi_jwt import JwtAuthorizationCredentials
from src.schemas.auth import (
    LoginResponse,
    LoginRequest,
    RegistrationResponse,
    RegistrationRequest,
    RefreshResponse,
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth_cookies import set_auth_cookies
from src.services.auth import AuthService
from src.utils.dependencies import get_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/registration", response_model=RegistrationResponse)
async def registration(data: RegistrationRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await AuthService.registration(db, data)
    set_auth_cookies(response, result.access_token, result.refresh_token)
    return RegistrationResponse(user=result.user)


@auth_router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await AuthService.login(db, data)
    set_auth_cookies(response, result.access_token, result.refresh_token)
    return LoginResponse(user=result.user)


@auth_router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(
    db: AsyncSession = Depends(get_db),
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
):
    return await AuthService.refresh(db, credentials)
