from fastapi import Response
from src.database.config import settings
from src.utils.security import access_security, refresh_security

#TODO: TAKING TOKENS FROM ENV
ACCESS_TOKEN_COOKIE = "access_token_cookie"
REFRESH_TOKEN_COOKIE = "refresh_token_cookie"


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=access_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=int(access_security.access_expires_delta.total_seconds()),
        path="/",
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE,
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=int(refresh_security.refresh_expires_delta.total_seconds()),
        path="/",
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(
        ACCESS_TOKEN_COOKIE,
        path="/",
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )
    response.delete_cookie(
        REFRESH_TOKEN_COOKIE,
        path="/",
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
    )
