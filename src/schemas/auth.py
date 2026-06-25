from pydantic import BaseModel, ConfigDict, Field, EmailStr
from src.schemas.user import UserRead

class RegistrationRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=4)

class RegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user: UserRead

class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    password: str = Field(min_length=4)

class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user: UserRead

class RefreshResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class AuthTokens(BaseModel):
    user: UserRead
    access_token: str
    refresh_token: str

