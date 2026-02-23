from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..utils import IS_DEV

from ..auth import create_access_token, get_password_hash, verify_password
from ..dependencies import get_current_user, require_user, require_superuser
from ..models import User, Profile, Settings
from ..schemas.generic import MessageResponse
from ..schemas.auth import BaseSettings, SignupRequest, TokenResponse, UserResponse


router: APIRouter = APIRouter(
    tags=["Auth"],
    include_in_schema=IS_DEV
)

@router.post("/auth/signup", response_model=TokenResponse)
async def signup(
    data: SignupRequest
) -> dict[str, str]:
    """
    Create a new user

    If this is the first user on the server, make them a superuser

    Paramaters:
        data (SignupRequest): The data to create the user

    Returns:
        TokenResponse: The access token
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

    access_token = create_access_token(data={"sub": str(user.uuid)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """
    OAuth2 compatible token login, get an access token for future requests

    Parameters:
        form_data (OAuth2PasswordRequestForm): The data to login with

    Returns:
        dict[str, str]: The access token
    """
    user: User | None = await User.get_or_none(username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token: str = create_access_token(data={"sub": str(user.uuid)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/", response_model=list[UserResponse])
async def get_users(user = Depends(require_superuser)) -> list[User]:
    """
    Get all users on the server

    Requires superuser access

    Returns:
        list[User]: A list of all users
    """
    users: list[User] = await User.all()
    return users

@router.delete("/users/delete/{username}", response_model=MessageResponse)
async def delete_user(username: str, user: User = Depends(require_user)) -> dict[str, str]:
    """
    Delete a user on the server

    Requires superuser access

    Parameters:
        username (str): The username of the user to delete

    Returns:
        MessageResponse: A message indicating that the user was deleted
    """
    user_to_delete: User | None = await User.get_or_none(username=username)

    if not user_to_delete:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        # Only be able to delete user if they are deleting themselves, or if they are a superuser
        if user_to_delete.uuid == user.uuid or user.is_superuser:        
            await user_to_delete.delete()
            return {"message": "User deleted"}
        else:
            raise HTTPException(status_code=403, detail="User not authorized to delete this user")

@router.get("/users/me/get_settings", response_model=BaseSettings)
async def get_user_settings(current_user: User = Depends(get_current_user)) -> Settings:
    """
    Get the settings for the current user

    Returns:
        BaseSettings: The settings for the current user
    """
    user: User | None = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    settings: Settings | None = await Settings.get_or_none(user=user)

    if not settings:
        settings = await Settings.create(user=user)
    return settings

@router.post("/users/me/update_settings", response_model=BaseSettings)
async def update_user_settings(data: BaseSettings, current_user: User = Depends(get_current_user)) -> Settings:
    """
    Update the settings for the current user

    Parameters:
        data (BaseSettings): The settings to update

    Returns:
        BaseSettings: The settings for the current user
    """
    user: User | None = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    settings: Settings | None = await Settings.get_or_none(user=user)

    if not settings:
        settings = await Settings.create(user=user)

    for key, value in data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
        else:
            print(f"Warning: ignoring unknown setting key '{key}'")

    await settings.save()
    return settings

@router.post("/users/set_superuser/{username}", response_model=UserResponse)
async def set_superuser(username: str, superuser: User = Depends(require_superuser)) -> User:
    """
    Set a user as a superuser

    Requires superuser access

    Parameters:
        username (str): The username of the user to set as a superuser

    Returns:
        User: The user that was set as a superuser
    """
    user_to_set_superuser: User | None = await User.get_or_none(username=username)

    if not user_to_set_superuser:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user_to_set_superuser.is_superuser = True
        await user_to_set_superuser.save()
        return user_to_set_superuser

@router.get("/auth/validate", response_model=UserResponse)
async def validate_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Validate the current user

    Returns:
        User: The current user
    """
    return current_user