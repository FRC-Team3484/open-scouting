from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator


class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    team_number: int
    display_name: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    uuid: UUID
    username: str
    email: EmailStr
    is_superuser: bool
    display_name: str
    team_number: int
    email_verified: bool
    created_at: datetime

# TODO: Can this take an arbitrary number of settings with any name?
class BaseSettings(BaseModel):
    favorite_events: list[str]

# Used in /auth/me, to return the user's current settings
class UserSetting(BaseModel):
    key: str
    value: Any | None
    description: str
    type: Literal["string", "number", "boolean", "json"]

class UserMeResponse(BaseModel):
    authenticated: bool
    user: UserResponse | None
    settings: list[UserSetting] | None
