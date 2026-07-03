from datetime import datetime
from typing import Any, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, create_model, model_validator

from ..setting_fields import ArraySetting, BooleanSetting, JSONSetting, NumberSetting, StringSetting
from ..models import Settings

def build_settings_schema():
    """
    Build a Pydantic model from the Settings model fields
    """
    model_fields = {}

    for name, field in Settings._meta.fields_map.items():
        if name in {"uuid", "user"}:
            continue

        # Map Tortoise field -> Python type
        if isinstance(field, StringSetting):
            field_type = str
        elif isinstance(field, NumberSetting):
            field_type = int
        elif isinstance(field, BooleanSetting):
            field_type = bool
        elif isinstance(field, ArraySetting):
            field_type = list
        elif isinstance(field, JSONSetting):
            field_type = object  # or list[str], dict, Any, etc.
        else:
            field_type = object

        model_fields[name] = (Optional[field_type], None)

    return create_model(
        "BaseSettings",
        __base__=BaseModel,
        **model_fields,
    )

class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    team_number: int
    display_name: str
    verification_code_uuid: UUID | None

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
    display_name: str | None
    team_number: int
    email_verified: bool
    profile_picture_url: str | None
    created_at: datetime

BaseSettings = build_settings_schema()

# Used in /auth/me, to return the user's current settings
class UserSetting(BaseModel):
    key: str
    value: Any | None
    name: str
    description: str | None
    section: str | None
    visible: bool
    type: Literal["string", "number", "boolean", "array", "json"]

class UserMeResponse(BaseModel):
    authenticated: bool
    user: UserResponse | None
    settings: list[UserSetting] | None
