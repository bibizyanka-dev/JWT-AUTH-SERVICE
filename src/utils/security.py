from datetime import timedelta

from fastapi_jwt import JwtAccessBearer, JwtRefreshBearer
from src.database.config import settings

access_security = JwtAccessBearer(
    secret_key=settings.JWT_SECRET,
    auto_error=True,
    access_expires_delta=timedelta(minutes=1440)
)

refresh_security = JwtRefreshBearer(
    secret_key=settings.JWT_SECRET,
    auto_error=True,
    refresh_expires_delta=timedelta(minutes=8640)
)