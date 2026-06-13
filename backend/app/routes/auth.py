from typing import Literal
from sqlite3 import IntegrityError
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import FieldError

from ..utils import IS_DEV

from ..auth import create_access_token, get_password_hash, verify_password
from ..dependencies import Identity, get_identity, require_user, require_superuser
from ..models import User, Profile, Settings, Session
from ..schemas.generic import MessageResponse
from ..schemas.auth import BaseSettings, SignupRequest, UserMeResponse, UserMeResponse, UserResponse, UserSetting


router: APIRouter = APIRouter(
    tags=["Auth"],
    include_in_schema=IS_DEV
)

def field_type_to_string(type: str) -> Literal["string", "number", "boolean", "array", "json"]:
    if type == "StringSetting":
        return "string"
    elif type == "NumberSetting":
        return "number"
    elif type == "BooleanSetting":
        return "boolean"
    elif type == "ArraySetting":
        return "array"
    elif type == "JSONSetting":
        return "json"
    else:
        return "json"

@router.get("/auth/me", response_model=UserMeResponse)
async def me(
    identity: Identity = Depends(get_identity)
):
    """
    Validates the current user, and returns their details

    Returns:
        UserMeResponse: The current user details, and whether they are authenticated or not
    """

    if identity.user:
        user = UserResponse(
            uuid=identity.user.uuid,
            username=identity.user.username,
            email=identity.user.email,
            is_superuser=identity.user.is_superuser,
            display_name=identity.profile.display_name,
            team_number=identity.profile.team_number,
            email_verified=identity.user.email_verified,
            created_at=identity.user.created_at
        )

        settings = await Settings.get_or_none(user=identity.user)
        settings_list: list[UserSetting] | None = []

        if settings:
            for key, field in Settings._meta.fields_map.items():
                if key in {"user", "uuid"}:
                    continue

                if key.endswith("_id"):
                    continue
                    
                settings_list.append(
                    UserSetting(
                        key=key,
                        value=getattr(settings, key),
                        name=field.display_name,
                        description=field.setting_description,
                        section=field.section,
                        visible=field.visible,
                        type=field_type_to_string(field.__class__.__name__),
                    )
                )

    else:
        user = None
        settings_list = None

    return UserMeResponse(
        authenticated=identity.user is not None,
        user=user,
        settings=settings_list
    )

@router.post("/auth/login", response_model=MessageResponse)
async def login(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Logs in a user

    Returns:
        MessageResponse: A message indicating that the user has been logged in
    """
    user = await User.get_or_none(
        username=form_data.username
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    session_id = request.cookies.get("session_id")

    session = None

    if session_id:
        session = await Session.get_or_none(
            uuid=session_id
        )

    if not session:
        session = await Session.create(
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent")
        )

    session.user = user
    await session.save()

    access_token = create_access_token(
        {
            "sub": str(user.uuid),
            "sid": str(session.uuid)
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not IS_DEV,  # False for local dev only
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    response.set_cookie(
        key="session_id",
        value=str(session.uuid),
        httponly=True,
        secure=not IS_DEV,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    return MessageResponse(message="Login successful")

@router.post("/auth/signup", response_model=MessageResponse)
async def signup(
    request: Request,
    response: Response,
    data: SignupRequest
):
    """
    Create a new user

    If this is the first user on the server, make them a superuser

    Paramaters:
        data (SignupRequest): The data to create the user

    Returns:
        MessageResponse: A message indicating that the user has been created
    """
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password: str = get_password_hash(data.password)

    try:
        user: User = await User.create(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password
        )
        await Profile.create(user=user, display_name=data.display_name, team_number=int(data.team_number))

        # If this is the first user on the server, make them a superuser
        if await User.all().count() == 1:
            user.is_superuser = True
            await user.save()
            print(f"User {user.username} is now a superuser, because this is the first user on the server")

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user: User | None = await User.get_or_none(username=data.username)

    session = await Session.create(
        user=user,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    access_token = create_access_token(
        {
            "sub": str(user.uuid),
            "sid": str(session.uuid)
        }
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=IS_DEV,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    response.set_cookie(
        key="session_id",
        value=str(session.uuid),
        httponly=True,
        secure=IS_DEV,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
    )

    return MessageResponse(message="Signup successful")

@router.post("/auth/logout", response_model=MessageResponse)
async def logout(response: Response):
    """
    Logs out a user
    """

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("session_id", path="/")

    return MessageResponse(message="Logout successful")

@router.get("/users/", response_model=list[UserResponse])
async def get_users(identity: Identity = Depends(require_superuser)) -> list[UserResponse]:
    """
    Get all users on the server

    Requires superuser access

    Returns:
        list[User]: A list of all users
    """
    user_list: list[UserResponse] = []
    users: list[User] = await User.all()

    for user in users:
        profile = await Profile.get_or_none(user=user)

        if profile:
            user_list.append(
                UserResponse(
                    uuid=user.uuid,
                    username=user.username,
                    email=user.email,
                    is_superuser=user.is_superuser,
                    display_name=profile.display_name,
                    team_number=profile.team_number,
                    email_verified=user.email_verified,
                    created_at=user.created_at
                )
            )
        else:
            print(f"WARN: User {user.username} ({user.uuid}) has no profile")
            user_list.append(
                UserResponse(
                    uuid=user.uuid,
                    username=user.username,
                    email=user.email,
                    is_superuser=user.is_superuser,
                    display_name="",
                    team_number=0,
                    email_verified=user.email_verified,
                    created_at=user.created_at
                )
            )

    return user_list

@router.delete("/users/delete/{uuid}", response_model=MessageResponse)
async def delete_user(uuid: UUID, identity: Identity = Depends(require_user)) -> dict[str, str]:
    """
    Delete a user on the server

    Requires superuser access

    Parameters:
        uuid (uuid): The uuid of the user to delete

    Returns:
        MessageResponse: A message indicating that the user was deleted
    """
    user_to_delete: User | None = await User.get_or_none(uuid=uuid)

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        # Only be able to delete user if they are deleting themselves, or if they are a superuser
        if user_to_delete.uuid == identity.user.uuid or identity.user.is_superuser:        
            await user_to_delete.delete()
            return {"message": "User deleted"}
        else:
            raise HTTPException(status_code=403, detail="User not authorized to delete this user")

@router.get("/users/me/get_settings", response_model=list[UserSetting])
async def get_user_settings(identity: Identity = Depends(require_user)) -> list[UserSetting]:
    """
    Get the settings for the current user

    Returns:
        BaseSettings: The settings for the current user
    """
    settings: Settings | None = await Settings.get_or_none(user=identity.user)
    settings_list: list[UserSetting] | None = []        

    if not settings:
        settings = await Settings.create(user=identity.user)

    for key, field in Settings._meta.fields_map.items():
        if key in {"user", "uuid"}:
            continue

        if key.endswith("_id"):
            continue
            
        settings_list.append(
            UserSetting(
                key=key,
                value=getattr(settings, key),
                name=field.display_name,
                description=field.setting_description,
                section=field.section,
                visible=field.visible,
                type=field_type_to_string(field.__class__.__name__),
            )
        )

    return settings_list

@router.post("/users/me/update_settings", response_model=BaseSettings)
async def update_user_settings(data: BaseSettings, identity: Identity = Depends(require_user)) -> Settings:
    """
    Update the settings for the current user

    Parameters:
        data (BaseSettings): The settings to update

    Returns:
        BaseSettings: The settings for the current user
    """
    settings: Settings | None = await Settings.get_or_none(user=identity.user)

    if not settings:
        settings = await Settings.create(user=identity.user)

    updates = data.model_dump(exclude_unset=True)

    try:
        for key, value in updates.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
            else:
                print(f"Warning: ignoring unknown setting key '{key}'")

        await settings.save()
    except FieldError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return settings

@router.post("/users/set_superuser/{uuid}", response_model=MessageResponse)
async def set_superuser(uuid: UUID, identity: Identity = Depends(require_superuser)) -> MessageResponse:
    """
    Set a user as a superuser

    Requires superuser access

    Parameters:
        uuid (uuid): The uuid of the user to set as a superuser

    Returns:
        User: The user that was set as a superuser
    """
    user_to_set_superuser: User | None = await User.get_or_none(uuid=uuid)

    if not user_to_set_superuser:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user_to_set_superuser.is_superuser = True
        await user_to_set_superuser.save()
        return MessageResponse(message="User set as superuser")

@router.post("/users/remove_superuser/{uuid}", response_model=MessageResponse)
async def remove_superuser(uuid: UUID, identity: Identity = Depends(require_superuser)) -> MessageResponse:
    """
    Remove a user as a superuser

    Requires superuser access

    Parameters:
        uuid (uuid): The uuid of the user to remove as a superuser

    Returns:
        User: The user that was removed as a superuser
    """
    user_to_remove_superuser: User | None = await User.get_or_none(uuid=uuid)

    if not user_to_remove_superuser:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user_to_remove_superuser.is_superuser = False
        await user_to_remove_superuser.save()
        return MessageResponse(message="User removed as superuser")

@router.post("/users/me/set_display_name", response_model=MessageResponse)
async def set_display_name(display_name: str, identity: Identity = Depends(require_user)) -> MessageResponse:
    """
    Set the display name for the current user

    Parameters:
        display_name (str): The display name to set

    Returns:
        MessageResponse: A message indicating that the display name was set
    """
    profile: Profile | None = await Profile.get_or_none(user=identity.user)

    if not profile:
        profile = await Profile.create(user=identity.user)

    profile.display_name = display_name
    await profile.save()

    return MessageResponse(message="Display name set")

@router.post("/users/me/set_team_number", response_model=MessageResponse)
async def set_team_number(team_number: int, identity: Identity = Depends(require_user)) -> MessageResponse:
    """
    Set the team number for the current user

    Parameters:
        team_number (int): The team number to set

    Returns:
        MessageResponse: A message indicating that the team number was set
    """
    profile: Profile | None = await Profile.get_or_none(user=identity.user)

    if not profile:
        profile = await Profile.create(user=identity.user)

    profile.team_number = team_number
    await profile.save()

    return MessageResponse(message="Team number set")