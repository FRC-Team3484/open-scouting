from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas.auth import BaseSettings, SignupRequest, TokenResponse, UserResponse, MessageResponse

from ..auth import create_access_token, get_password_hash, verify_password
from ..dependencies import get_current_user, require_user
from ..models import User, Profile, Settings

router: APIRouter = APIRouter(
    tags=["Auth"],
    dependencies=[Depends(require_user)],
)

@router.post("/auth/signup", response_model=TokenResponse)
async def signup(
    data: SignupRequest
):
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = get_password_hash(data.password)

    try:
        user = await User.create(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password
        )
        await Profile.create(user=user, display_name=data.display_name, team_number=int(data.team_number))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = await User.get_or_none(username=data.username)

    access_token = create_access_token(data={"sub": str(user.uuid)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    user = await User.get_or_none(username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": str(user.uuid)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/", response_model=list[UserResponse])
async def read_items() -> list[User]:
    users = await User.all()
    return users

@router.delete("/users/delete/{username}", response_model=MessageResponse)
async def delete_user(username: str) -> dict[str, str]:
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return {"message": "User deleted"}

@router.get("/users/me/get_settings", response_model=BaseSettings)
async def get_user_settings(current_user: User = Depends(get_current_user)) -> Settings:
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    settings = await Settings.get_or_none(user=user)

    if not settings:
        settings = await Settings.create(user=user)
    return settings

@router.post("/users/me/update_settings", response_model=BaseSettings)
async def update_user_settings(data: BaseSettings, current_user: User = Depends(get_current_user)) -> Settings:
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    settings = await Settings.get_or_none(user=user)

    if not settings:
        settings = await Settings.create(user=user)

    for key, value in data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
        else:
            print(f"Warning: ignoring unknown setting key '{key}'")

    await settings.save()
    return settings

@router.post("/users/me/set_superuser", response_model=UserResponse)
async def set_superuser(current_user: User = Depends(get_current_user)) -> User:
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_superuser = True
    await user.save()
    return user

@router.get("/auth/validate", response_model=UserResponse)
async def validate_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user