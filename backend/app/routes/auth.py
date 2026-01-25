from sqlite3 import IntegrityError
from fastapi import APIRouter, Body, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.contrib.pydantic import pydantic_model_creator

from ..auth import create_access_token, get_password_hash, verify_password
from ..dependencies import get_current_user
from ..models import User, Profile, Settings

router: APIRouter = APIRouter()
UserOut = pydantic_model_creator(User, name="UserOut", exclude=["hashed_password"])


@router.post("/auth/signup")
async def signup(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    team_number: str = Form(...),
    display_name: str = Form(...)
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = get_password_hash(password)

    try:
        user = await User.create(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        await Profile.create(user=user, display_name=display_name, team_number=int(team_number))
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = await User.get_or_none(username=username)

    access_token = create_access_token(data={"sub": str(user.uuid)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": str(user.uuid)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/")
async def read_items(current_user: User = Depends(get_current_user), response_model=UserOut):
    users = await User.all()
    return users

@router.delete("/users/delete/{username}")
async def delete_user(username: str, current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return {"message": "User deleted"}

@router.get("/users/me/get_settings")
async def get_user_settings(current_user: User = Depends(get_current_user), response_model=UserOut):
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    settings = await Settings.get_or_none(user=user)

    if not settings:
        settings = await Settings.create(user=user)
    return settings

@router.post("/users/me/update_settings")
async def update_user_settings(settings_data: dict = Body(...), current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    settings = await Settings.get_or_none(user=user)

    if not settings:
        settings = await Settings.create(user=user)

    for key, value in settings_data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
        else:
            print(f"Warning: ignoring unknown setting key '{key}'")

    await settings.save()
    return settings

@router.post("/users/me/set_superuser")
async def set_superuser(current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_superuser = True
    await user.save()
    return user

@router.get("/auth/validate")
async def validate_user(current_user: User = Depends(get_current_user), response_model=UserOut):
    return current_user