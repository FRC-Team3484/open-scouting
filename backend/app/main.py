import os
from datetime import timedelta

from pydantic import BaseModel
from typing import Annotated

from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError

from app.models import User, Profile, Organization, OrganizationMember
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

    user = await User.get_or_none(username=username)

    access_token = create_access_token(data={"sub": str(user.uuid)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": str(user.uuid)})
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await User.get_or_none(uuid=payload.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# Example protected route
@app.get("/users/")
async def read_items(current_user: User = Depends(get_current_user), response_model_exclude={"hashed_password"}):
    users = await User.all()
    return users

@app.delete("/users/delete/{username}")
async def delete_user(username: str, current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return {"message": "User deleted"}

@app.get("/auth/validate")
async def validate_user(current_user: User = Depends(get_current_user), response_model_exclude={"hashed_password"}):
    return current_user

# Organizations
@app.post("/organization/create")
async def create_organization(name: str = Form(...), label: str = Form(...), description: str = Form(...), current_user: User = Depends(get_current_user)):
    organization = await Organization.create(name=name, label=label, description=description)
    await OrganizationMember.create(organization=organization, user=current_user, role="admin")
    return organization

@app.get("/organization/all/list")
async def get_organizations(current_user: User = Depends(get_current_user), response_model_exclude={"hashed_password"}):
    organizations = await Organization.all()
    return organizations

@app.get("/organization/me/list")
async def get_user_organizations(current_user: User = Depends(get_current_user), response_model_exclude={"hashed_password"}):
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    organization_members = await OrganizationMember.filter(user=user)
    organizations = await Organization.filter(uuid__in=[m.organization_id for m in organization_members])

    return organizations

@app.get("/organization/{organization_uuid}")
async def get_organization(organization_uuid: str, current_user: User = Depends(get_current_user), response_model_exclude={"hashed_password"}):
    organization = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@app.delete("/organization/delete/{organization_uuid}")
async def delete_organization(organization_uuid: str, current_user: User = Depends(get_current_user)):
    organization = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    await organization.delete()
    return {"message": "Organization deleted"}

@app.get("/organization/{organization_uuid}/members")
async def get_organization_members(organization_uuid: str, current_user: User = Depends(get_current_user), response_model_exclude={"hashed_password"}):
    organization = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    members = await OrganizationMember.filter(organization=organization)
    return members