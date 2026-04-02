from fastapi import HTTPException
import pytest
from types import SimpleNamespace
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.auth import RegistrationRequest, RegistrationResponse, LoginResponse, LoginRequest
from src.services.auth import AuthService

@pytest.mark.asyncio
async def test_user_success_registration(db: AsyncSession):
    result: RegistrationResponse = await AuthService.registration(
        db, RegistrationRequest(email="test228@gmail.com", username="test_username", password="fake_password")
    )

    assert result is not None
    assert result.user.username == "test_username"
    assert result.access_token != ""
    assert result.refresh_token != ""
    assert isinstance(result, RegistrationResponse)
    assert isinstance(result.access_token, str)
    assert isinstance(result.refresh_token, str)

@pytest.mark.asyncio
async def test_user_registration_already_exists(db: AsyncSession):
    await AuthService.registration(
        db, RegistrationRequest(email="test228@gmail.com", username="test_username", password="fake_passowrd")
    )

    with pytest.raises(HTTPException) as exc_info:
        await AuthService.registration(
            db, RegistrationRequest(email="test228@gmail.com", username="test_username", password="fake_password")
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "User already exists"


@pytest.mark.asyncio
async def test_user_success_login(db: AsyncSession):
    await AuthService.registration(
        db, RegistrationRequest(email="test228@gmail.com", username="test_username", password="fake_password")
    )

    result: LoginResponse = await AuthService.login(
        db, LoginRequest(email="test228@gmail.com", username="test_username", password="fake_password")
    )

    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.token_type == "bearer"
    assert result.user.username == "test_username"


@pytest.mark.asyncio
async def test_user_unsuccess_login_with_password(db: AsyncSession):
    await AuthService.registration(
        db, RegistrationRequest(email="test228@gmail.com", username="test_username", password="fake_password")
    )

    with pytest.raises(HTTPException) as exc_info:
        await AuthService.login(
            db, LoginRequest(email="test228@gmail.com", username="test_username", password="fake_password_fake_password")
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid username or password"

@pytest.mark.asyncio
async def test_user_unsuccess_login_with_username(db: AsyncSession):
    await AuthService.registration(
        db, RegistrationRequest(email="test228@gmail.com", username="test_username", password="fake_password")
    )

    with pytest.raises(HTTPException) as exc_info:
        await AuthService.login(
            db, LoginRequest(email="test228@gmail.com", username="test_username_1", password="fake_password")
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid username or password"

@pytest.mark.asyncio
async def test_user_refresh(db: AsyncSession):
    registration_result = await AuthService.registration(
        db, RegistrationRequest(email="test228@gmail.com", username="test_username", password="fake_password")
    )

    credentials = SimpleNamespace(
        subject={
            "sub": str(registration_result.user.id),
            "username": registration_result.user.username,
            "type": "refresh"
        }
    )

    result = await AuthService.refresh(db, credentials)

    assert result.access_token is not None
    assert result.refresh_token is not None
    assert result.token_type == "bearer"

@pytest.mark.asyncio
async def test_user_refresh_invalid_token(db: AsyncSession):
    credentials = SimpleNamespace(
        subject={
            "sub": "999999",
            "username": "ghost",
            "type": "refresh",
        }
    )

    with pytest.raises(HTTPException) as exc_info:
        await AuthService.refresh(db, credentials)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"