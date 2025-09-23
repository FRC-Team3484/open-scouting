import os
from datetime import timedelta

from pydantic import BaseModel
from typing import Annotated

from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError

from app.models import User, Profile
from app.auth import get_password_hash, verify_password, create_access_token, decode_access_token

# Setup
app = FastAPI()

origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL", "sqlite://dev.db"),
    modules={"models": ["app.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)

TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL", "sqlite://dev.db")},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

# Routes
#    Auth
@app.post("/auth/signup")
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

    return {"success": True, "message": f"Account created for {username}"}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await User.get_or_none(id=int(payload.get("sub")))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# Example protected route
@app.get("/items/")
async def read_items(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}