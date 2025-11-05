import os
from datetime import timedelta

from pydantic import BaseModel
from typing import Annotated, List

from fastapi import FastAPI, Form, Depends, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import User, Profile, Organization, OrganizationMember, Season, Settings, GamePiece, MatchScoutingField
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

# Model Schemas
UserOut = pydantic_model_creator(User, name="UserOut", exclude=["hashed_password"])

# Utility Functions
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await User.get_or_none(uuid=payload.get("sub"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

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

@app.get("/users/")
async def read_items(current_user: User = Depends(get_current_user), response_model=UserOut):
    users = await User.all()
    return users

@app.delete("/users/delete/{username}")
async def delete_user(username: str, current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return {"message": "User deleted"}

@app.get("/users/me/get_settings")
async def get_user_settings(current_user: User = Depends(get_current_user), response_model=UserOut):
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    settings = await Settings.get_or_none(user=user)

    if not settings:
        settings = await Settings.create(user=user)
    return settings

@app.post("/users/me/update_settings")
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

@app.post("/users/me/set_superuser")
async def set_superuser(current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_superuser = True
    await user.save()
    return user

@app.get("/auth/validate")
async def validate_user(current_user: User = Depends(get_current_user), response_model=UserOut):
    return current_user

#    Organizations
@app.post("/organization/create")
async def create_organization(name: str = Form(...), description: str = Form(...), current_user: User = Depends(get_current_user)):
    organization = await Organization.create(name=name, description=description)
    await OrganizationMember.create(organization=organization, user=current_user, role="admin")
    return organization

@app.get("/organization/all/list")
async def get_organizations():
    organizations = await Organization.all()
    return organizations

@app.get("/organization/me/list")
async def get_user_organizations(current_user: User = Depends(get_current_user)):
    user = await User.get_or_none(uuid=current_user.uuid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    organization_members = await OrganizationMember.filter(user=user)
    organizations = await Organization.filter(uuid__in=[m.organization_id for m in organization_members])

    return organizations

@app.get("/organization/{organization_uuid}")
async def get_organization(organization_uuid: str):
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
async def get_organization_members(organization_uuid: str, current_user: User = Depends(get_current_user)):
    organization = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    members = await OrganizationMember.filter(organization=organization)
    return members

#    Seasons
@app.get("/seasons")
async def get_seasons():
    seasons = await Season.all()
    return seasons

@app.get("/seasons/active")
async def get_active_season():
    season = await Season.get_or_none(active=True)
    return season

@app.post("/seasons/create")
async def create_season(year: int = Form(...), name: str = Form(...), active: bool = Form(...), current_user: User = Depends(get_current_user)):
    season = await Season.create(year=year, name=name, active=active)
    return season

@app.delete("/seasons/delete/{season_uuid}")
async def delete_season(season_uuid: str, current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    await season.delete()
    return {"message": "Season deleted"}

#    Game Pieces
@app.get("/gamepieces")
async def get_gamepieces():
    gamepieces = await GamePiece.all()
    return gamepieces

@app.post("/gamepieces/create")
async def create_gamepiece(season_uuid: str = Form(...), name: str = Form(...), current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    gamepiece = await GamePiece.create(season=season, name=name)
    return gamepiece

@app.get("/gamepieces/season/{season_uuid}")
async def get_season_gamepieces(season_uuid: str):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    gamepieces = await GamePiece.filter(season=season)
    return gamepieces

@app.delete("/gamepieces/delete/{gamepiece_uuid}")
async def delete_gamepiece(gamepiece_uuid: str, current_user: User = Depends(get_current_user)):
    gamepiece = await GamePiece.get_or_none(uuid=gamepiece_uuid)
    if not gamepiece:
        raise HTTPException(status_code=404, detail="Game piece not found")
    await gamepiece.delete()
    return {"message": "Game piece deleted"}

#    Match Scouting Fields
@app.get("/fields/season/{season_uuid}")
async def get_season_fields(season_uuid: str):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    fields = await MatchScoutingField.filter(season=season)
    return fields

@app.post("/fields/season/{season_uuid}/create")
async def create_season_field(season_uuid: str, name: str = Form(...), field_type: str = Form(...), stat_type: str = Form(...), game_piece_uuid: str = Form(...), required: bool = Form(...), options: list = Form(...), order: int = Form(...), organization_uuid: str = Form(...), parent_uuid: str = Form(...), current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    game_piece = await GamePiece.get_or_none(uuid=game_piece_uuid)
    if not game_piece:
        raise HTTPException(status_code=404, detail="Game piece not found")
    if organization_uuid != "":
        organization = await Organization.get_or_none(uuid=organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    if parent_uuid != "":
        parent = await MatchScoutingField.get_or_none(uuid=parent_uuid)
        if not section:
            raise HTTPException(status_code=404, detail="Section not found")
    else:
        section = None

    field = await MatchScoutingField.create(season=season, name=name, field_type=field_type, stat_type=stat_type, game_piece=game_piece, required=required, options=options, order=order, organization=organization, section=section)
    return field

@app.post("/fields/season/{season_uuid}/edit/{field_uuid}")
async def edit_season_field(season_uuid: str, field_uuid: str, name: str = Form(...), field_type: str = Form(...), stat_type: str = Form(...), game_piece_uuid: str = Form(...), required: bool = Form(...), options: list = Form(...), order: int = Form(...), organization_uuid: str = Form(...), current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    field = await MatchScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    game_piece = await GamePiece.get_or_none(uuid=game_piece_uuid)
    if not game_piece:
        raise HTTPException(status_code=404, detail="Game piece not found")
    organization = await Organization.get_or_none(uuid=organization_uuid)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    field.name = name
    field.field_type = field_type
    field.stat_type = stat_type
    field.game_piece = game_piece
    field.required = required
    field.options = options
    field.order = order
    field.organization = organization
    await field.save()
    return field

@app.delete("/fields/delete/{field_uuid}")
async def delete_field(field_uuid: str, current_user: User = Depends(get_current_user)):
    field = await MatchScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    await field.delete()
    return {"message": "Field deleted"}