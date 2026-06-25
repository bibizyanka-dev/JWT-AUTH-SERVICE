from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from src.utils.annotated import Locale

class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    username: str
    locale: Locale | None = None

class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    username: str
    password: str
    avatar_url: str

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    locale: Locale | None = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str | None):
        if value is not None and not value.strip():
            raise ValueError("Username cannot be empty")
        return value
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str | None):
        if value is not None and len(value) < 8:
            raise ValueError("Password must be at least 8 character long")
        return value