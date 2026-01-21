from collections import defaultdict
import json
import os
import pprint
from statistics import mean
from time import strftime
from typing import List, Optional
import uuid
from dotenv import load_dotenv
import requests
from pathlib import Path
import httpx

from fastapi import FastAPI, Form, Depends, HTTPException, Query, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import IntegrityError
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models import \
    MatchScoutingSubmission, \
    User, \
    Profile, \
    Organization, \
    OrganizationMember, \
    Season, \
    Settings, \
    GamePiece, \
    MatchScoutingField, \
    Event, \
    MatchScoutingAnswer, \
    PitScoutingField, \
    TeamPit, \
    PitScoutingAnswer

from app.auth import get_password_hash, verify_password, create_access_token, decode_access_token

# Setup
app = FastAPI(root_path="/api")

load_dotenv()
ENV = os.getenv("ENV", "development")

origins = os.getenv("CORS_ORIGINS", "*").split(",")
TBA_API_KEY = os.getenv("TBA_API_KEY")

if TBA_API_KEY is None or TBA_API_KEY == "":
    print("TBA_API_KEY is not set. Pit scouting will not work as expected.")

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
    db_url=os.getenv("DATABASE_URL", "postgres://app:app@localhost:5432/app"),
    modules={"models": ["app.models"]},
    generate_schemas=False,
    add_exception_handlers=True,
)

TORTOISE_ORM = {
    "connections": {"default": os.getenv("DATABASE_URL", "postgres://app:app@localhost:5432/app")},
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
    # Find the season
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    # Fetch all fields for the season including their children
    fields = await MatchScoutingField.filter(season=season).prefetch_related("children")

    # Convert queryset to list of dicts
    field_list = [f for f in fields]

    # Build lookup dict for fast parent-child linking
    field_map = {f.uuid: f for f in field_list}

    # Prepare the tree structure
    tree = []

    # Attach children recursively
    for field in field_list:
        # Convert model instance to dict
        field_data = {
            "uuid": str(field.uuid),
            "name": field.name,
            "field_type": field.field_type,
            "stat_type": field.stat_type,
            "game_piece_id": str(field.game_piece_id) if field.game_piece_id else None,
            "required": field.required,
            "options": field.options,
            "order": field.order,
            "organization_id": str(field.organization_id) if field.organization_id else None,
            "fields": []  # for children
        }

        # If field has a parent, attach it to parent's "fields" list
        if field.parent_id:
            parent = field_map.get(field.parent_id)
            if not hasattr(parent, "_tree_fields"):
                parent._tree_fields = []
            parent._tree_fields.append(field_data)
        else:
            # Top-level field (no parent)
            tree.append(field_data)

        # Store the built dict for later child assignment
        field._tree_data = field_data

    # Now attach children properly to their parents' dicts
    for field in field_list:
        if hasattr(field, "_tree_fields"):
            field._tree_data["fields"] = field._tree_fields

    # Sort recursively by `order`
    def sort_fields(fields):
        fields.sort(key=lambda f: f["order"])
        for f in fields:
            sort_fields(f["fields"])

    sort_fields(tree)

    return tree

@app.delete("/fields/season/{season_uuid}/clear")
async def clear_season_fields(season_uuid: str, current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    await MatchScoutingField.filter(season=season).delete()
    return {"message": "Fields cleared"}

@app.post("/fields/season/{season_uuid}/create")
async def create_season_field(
        season_uuid: str, 
        name: str = Form(...), 
        field_type: str = Form(...), 
        stat_type: str = Form(...), 
        game_piece_uuid: str = Form(...), 
        required: bool = Form(...), 
        options: list = Form(...),
        order: int = Form(...), 
        organization_uuid: str = Form(...), 
        parent_uuid: str = Form(...), 
        current_user: User = Depends(get_current_user)
    ):

    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    if stat_type == "auton_score" or stat_type == "auton_miss" or stat_type == "teleop_score" or stat_type == "teleop_miss":
        game_piece = await GamePiece.get_or_none(uuid=game_piece_uuid)
        if not game_piece:
            
            # Temporary hack to try and repair game pieces for imported fields
            # TODO: Replace this later for proper game piece repairing in the edit dialog
            game_pieces = await GamePiece.all()
            matching_game_pieces = [gp for gp in game_pieces if any(word in name.split() for word in gp.name.split())]
            
            if matching_game_pieces:
                print("WARNING: Game piece not found. Using closest match based on field name: " + matching_game_pieces[0].name)
                game_piece = matching_game_pieces[0]
            else:
                raise HTTPException(status_code=404, detail="Game piece not found")
    else:
        game_piece = None

    if organization_uuid != "":
        organization = await Organization.get_or_none(uuid=organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    if parent_uuid != "":
        parent = await MatchScoutingField.get_or_none(uuid=parent_uuid)
        if not parent:
            raise HTTPException(status_code=404, detail="Section not found")
    else:
        parent = None

    field = await MatchScoutingField.create(
        parent=parent,
        season=season, 
        name=name, 
        field_type=field_type, 
        stat_type=stat_type, 
        game_piece=game_piece, 
        required=required, 
        options=options, 
        order=order, 
        organization=organization
    )
    return field

@app.post("/fields/season/{season_uuid}/edit/{field_uuid}")
async def edit_season_field(
        season_uuid: str, 
        field_uuid: str, 

        parent_uuid: str = Form(...),
        name: str = Form(...), 
        field_type: str = Form(...), 
        stat_type: str = Form(...), 
        game_piece_uuid: str = Form(...), 
        required: bool = Form(...), 
        options: list = Form(...), 
        order: int = Form(...), 
        organization_uuid: str = Form(...), 
        current_user: User = Depends(get_current_user)
    ):

    field = await MatchScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
        
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    if stat_type == "auton_score" or stat_type == "auton_miss" or stat_type == "teleop_score" or stat_type == "teleop_miss":
        game_piece = await GamePiece.get_or_none(uuid=game_piece_uuid)
        if not game_piece:
            raise HTTPException(status_code=404, detail="Game piece not found")
    else:
        game_piece = None

    if organization_uuid != "":
        organization = await Organization.get_or_none(uuid=organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

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

@app.get("/fields/get_presets")
async def get_match_scouting_field_presets():    
    print(os.getcwd())
    path = Path("./app/match_scouting_presets")
    presets = []

    for file in path.iterdir():
        with open(file, "r") as f:
            presets.append({ "name": file.stem, "preset": json.load(f) })

    return presets

@app.delete("/fields/delete/{field_uuid}")
async def delete_field(field_uuid: str, current_user: User = Depends(get_current_user)):
    field = await MatchScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    await field.delete()
    return {"message": "Field deleted"}

#    Match Scouting Answers
@app.post("/scouting/submit")
async def submit_match_scouting(
    submission_uuid: str = Form(...),
    fields: str = Form(...),
    user_uuid: str = Form(...), # Is either the UUID for the authenticated user, or just a username
    year: int = Form(...),
    team_number: int = Form(...),
    match_number: int = Form(...),
    match_type: str = Form(...),
    event_code: str = Form(...),
    event_name: str = Form(...),
    event_type: str = Form(...),
    event_city: str = Form(...),
    event_country: str = Form(...),
    event_start_date: str = Form(...),
    event_end_date: str = Form(...)
):
    fields = json.loads(fields)

    if user_uuid != "":
        user = await User.get_or_none(uuid=user_uuid)
        if not user:
            user = None # Sets the user to none if not a user. This should probably be the user's username later
    else:
        user = None

    season = await Season.get_or_none(year=year)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    event, _ = await Event.get_or_create(
        season=season,
        event_code=event_code,
        name=event_name,
        type=event_type,
        city=event_city,
        country=event_country,
        start_date=event_start_date,
        end_date=event_end_date
    )

    try:
        submission = await MatchScoutingSubmission.create(
            uuid=submission_uuid,
            user=user,
            event=event,
            team_number=team_number,
            match_number=match_number,
            match_type=match_type
        )
    except IntegrityError:
        raise HTTPException(status_code=200, detail="Submission already exists")

    for key, value in fields.items():
        field = await MatchScoutingField.get_or_none(uuid=key)
        if not field:
            raise HTTPException(status_code=404, detail="Field not found")

        _ = await MatchScoutingAnswer.create(
            field=field,
            value=json.dumps(value),
            submission=submission
        )

    return submission

#    Pit Scouting
@app.get("/pits/fields/{season_uuid}")
async def get_pit_fields(season_uuid: str):
    season = await Season.get_or_none(uuid=season_uuid)

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    fields = await PitScoutingField.filter(season=season)
    return fields

@app.delete("/pits/fields/{season_uuid}/clear")
async def clear_pit_fields(season_uuid: str, current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    await PitScoutingField.filter(season=season).delete()
    return {"message": "Fields cleared"}

@app.post("/pits/fields/{season_uuid}/create")
async def create_pit_field(
    season_uuid: str,

    name: str = Form(...),
    field_type: str = Form(...),
    options: str = Form(...),
    order: int = Form(...),
    organization_uuid: str = Form(...)
    ):

    print(options)

    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    if organization_uuid != "":
        organization = await Organization.get_or_none(uuid=organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    field = await PitScoutingField.create(
        season=season,
        name=name,
        field_type=field_type,
        options=options,
        order=order,
        organization=organization
    )
    return field

@app.patch("/pits/fields/{season_uuid}/edit/{field_uuid}")
async def edit_pit_field(
    season_uuid: str, 
    field_uuid: str,

    name: str = Form(...),
    field_type: str = Form(...),
    options: str = Form(...),
    order: int = Form(...),
    organization_uuid: str = Form(...)
    
    ):
    
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    field = await PitScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    if organization_uuid != "":
        organization = await Organization.get_or_none(uuid=organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    field.name = name
    field.field_type = field_type
    field.options = options
    field.order = order
    field.organization = organization

    await field.save()
    return field

@app.delete("/pits/fields/{field_uuid}/delete")
async def delete_pit_field(
        field_uuid: str, 
        current_user: User = Depends(get_current_user)
    ):

    field = await PitScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    await field.delete()
    return field

@app.post("/pits/get/{season_uuid}")
async def get_pits(
    season_uuid: str, 
    
    event_code: str = Form(...),
    event_name: str = Form(...),
    event_type: str = Form(...),
    event_city: str = Form(...),
    event_country: str = Form(...),
    event_start_date: str = Form(...),
    event_end_date: str = Form(...)
    ):
    
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    event, _ = await Event.get_or_create(
        season=season,
        event_code=event_code,
        name=event_name,
        type=event_type,
        city=event_city,
        country=event_country,
        start_date=event_start_date,
        end_date=event_end_date
    )

    # If pits have not been generated yet, get teams from TBA and create TeamPits
    if not event.pits_generated and TBA_API_KEY != "" and TBA_API_KEY is not None and event.custom is False:
        event_key = str(season.year) + event_code
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"https://www.thebluealliance.com/api/v3/event/{event_key}/teams",
                headers={"X-TBA-Auth-Key": TBA_API_KEY},
            )

        teams = response.json()

        for team in teams:
            _ = await TeamPit.create(
                team_number=team["team_number"],
                nickname=team["nickname"],
                season=season,
                event=event
            )

        event.pits_generated = True
        await event.save()

    pits = await TeamPit.filter(event=event).prefetch_related("answers")
    return [
        {
            "uuid": pit.uuid,
            "team_number": pit.team_number,
            "nickname": pit.nickname,
            "created_at": pit.created_at,
            "answers": [
                {
                    "uuid": ans.uuid,
                    "field_uuid": ans.field_id,
                    "value": ans.value,
                    "username": ans.username,
                    "created_at": ans.created_at
                }
                for ans in pit.answers
            ]
        }
        for pit in pits
    ]

@app.post("/pits/submit/{season_uuid}/{team_number}")
async def submit_pit(
    season_uuid: str, 
    team_number: int,

    event_code: str = Form(...),
    event_name: str = Form(...),
    event_type: str = Form(...),
    event_city: str = Form(...),
    event_country: str = Form(...),
    event_start_date: str = Form(...),
    event_end_date: str = Form(...),

    answers: str = Form(...),
    nickname: str = Form(...)
    ):
    """
    Get the season and event from the uuids. Then, check if a pit with that team number exists.
    If it does, update that pit

    For the answers in that pit, find each answer that does not already exist on the server, and add them

    If a pit does not exist, that means it was created by the client of a user. It should be created.
    """
    
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    event = await Event.get_or_none(event_code=event_code, season=season).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    pit, created = await TeamPit.get_or_create(
        team_number=team_number,
        season=season,
        event=event,
        nickname=nickname
    )

    if created:
        print("Created pit", pit.uuid, "for team", team_number, "and event", event.uuid)

    for answer in json.loads(answers):
        field = await PitScoutingField.get_or_none(uuid=answer["field_uuid"])

        if not field:
            raise HTTPException(status_code=404, detail="Field not found")

        _, created = await PitScoutingAnswer.get_or_create(
            uuid=answer["uuid"],
            team=pit,
            field=field,
            value=answer["value"],
            username=answer["username"]
        )

        if created:
            print("Created answer", answer["uuid"], "for pit", pit.uuid, "and field", field.uuid)

    return

#    Data View
@app.get("/data/filters")
async def get_data_filters(
    year: int,
    event_codes: Optional[List[str]] = Query(None),
    team_numbers: Optional[List[int]] = Query(None),
    ):
    """
    For a year, list of event codes, and list of team numbers, return a JSON object 
        containing the available filters that can additionally be applied

    For example, if just a year is given, return all team numbers and events with data on the server.
    If a year and event code is given, return all team numbers for that event and year with data on the server.
    If a year and multiple event codes are given, return all team numbers which have data on the server for those event codes and year.
    If a year and a team number is given, return all event codes which have data on the server for that team number and year.
    If a year and multiple team numbers are given, return all event codes which have data on the server for those team numbers and year.
    """
    season = await Season.get_or_none(year=year)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    qs = MatchScoutingSubmission.filter(
        event__season=season
    ).select_related("event")

    if event_codes:
        qs = qs.filter(event__event_code__in=event_codes)

    if team_numbers:
        qs = qs.filter(team_number__in=team_numbers)

    events = await qs.distinct().values(
        event_code="event__event_code",
        event_name="event__name",
    )

    # TEAMS
    teams = await qs.distinct().values(
        team_number="team_number"
    )

    return {
        "events": events,
        "teams": teams,
    }

@app.get("/data/get")
async def get_data(
    year: int,
    event_codes: Optional[List[str]] = Query(None),
    team_numbers: Optional[List[int]] = Query(None),
):
    """
    Given a year, event codes, and team numbers, return the data that matches those filters

    Data should be structured based on the stat_type and game_piece of the associated MatchScoutingField.
    The data should be a list of JSON objects. Each object represents a team with data. In that object,
        there should be four lists: teleop, auton, capability, other
    teleop and auton should be a list of JSON objects, for each game_piece for that season.
        Then, for each game piece, it should be a list of JSON objects that represents each individual field with type: auton_score, auton_miss, teleop_score, teleop_miss
        These fields should have the field type, name, uuid, list of all data points, and the minimum, the maximum, and the average (if applicable).
    
    For example, there are two game pieces. Coral and Algae. There is a field for how much coral was scored and how much were dropped, both as a teleop_score.
        There will be a list of JSON objects for each team. In the team object, inside the teleop list, there should be two additional lists, one for coral and one for algae.
        Then there will two more JSON objects for both of those fields, with the field type, name, uuid, and list of all data points.

    Next, for capabilities, find each field that is a capability and find the percentages of each value occurrence. This will most likely 
        be something that is a multiple_choice or choice MatchScoutingField, and we'll want to show how often each value occurred using something like a pie chart.

    Finally, for other, simply return the same field information and the value, as this will likely be a text input.

    [
        {
            "team_number": 1234,
            "nickname": "Team 1234",
            "teleop": [
                "coral": [
                    {
                        "field_uuid": "uuid",
                        "field_type": "small_number",
                        "field_name": "Coral scored",
                        "values": [1, 2, 3, ...],
                        "min": 0,
                        "max": 100,
                        "avg": 50
                    },
                    {
                        "field_uuid": "uuid",
                        "field_type": "small_number",
                        "field_name": "Coral dropped",
                        "values": [1, 2, 3, ...],
                        "min": 0,
                        "max": 100,
                        "avg": 50
                    }
                ],
                "algae": [...],
            ],
            "auton": [...],
            "capability": [
                {
                    "field_uuid": "uuid",
                    "field_type": "choice",
                    "field_name": "Climb level",
                    "values": ["low", "medium", "high"],
                    "percentages": [
                        {
                            "value": "low",
                            "percentage": 50
                        }, {
                            "value": "medium",
                            "percentage": 25
                        }, {
                            "value": "high",
                            "percentage": 25
                        }
                    ],
                    ...
                }
            ],
            "other": [
                {
                    "field_uuid": "uuid",
                    "field_type": "string",
                    "field_name": "Notes",
                    "value": "Some notes",
                },
                ...
            ]
        },
        ...
    ]
    """

    season = await Season.get_or_none(year=year)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    submissions_qs = MatchScoutingSubmission.filter(
        event__season=season
    ).select_related("event")

    if event_codes:
        submissions_qs = submissions_qs.filter(event__event_code__in=event_codes)

    if team_numbers:
        submissions_qs = submissions_qs.filter(team_number__in=team_numbers)

    submissions = await submissions_qs

    if not submissions:
        return []

    submission_ids = [s.uuid for s in submissions]

    answers = await MatchScoutingAnswer.filter(
        submission_id__in=submission_ids,
        field__stat_type__not="ignore",
    ).select_related(
        "field",
        "field__game_piece",
        "submission",
    )

    # Load team nicknames from TeamPit (best available source)
    team_pits = await TeamPit.filter(
        season=season,
        team_number__in={s.team_number for s in submissions}
    )

    team_names = {
        tp.team_number: tp.nickname for tp in team_pits
    }

    # ------------------------
    # Data structure
    # ------------------------
    teams = defaultdict(lambda: {
        "team_number": None,
        "nickname": None,
        "teleop": defaultdict(list),
        "auton": defaultdict(list),
        "capability": [],
        "other": [],
    })

    # Helper: numeric conversion
    def parse_number(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    # ------------------------
    # Aggregate raw values
    # ------------------------
    field_values = defaultdict(list)

    for ans in answers:
        team_number = ans.submission.team_number
        field = ans.field

        teams[team_number]["team_number"] = team_number
        teams[team_number]["nickname"] = team_names.get(team_number)

        key = (team_number, field.uuid)
        field_values[key].append({
            "match_number": ans.submission.match_number,
            "value": json.loads(ans.value),
        })
        field_values[key] = sorted(field_values[key], key=lambda x: x["match_number"])

    # ------------------------
    # Process fields
    # ------------------------
    fields = await MatchScoutingField.filter(
        season=season,
        stat_type__not="ignore"
    ).select_related("game_piece")

    fields_by_uuid = {f.uuid: f for f in fields}

    for (team_number, field_uuid), raw_values in field_values.items():
        field = fields_by_uuid[field_uuid]
        stat_type = field.stat_type

        # NUMERIC (auton / teleop)
        if stat_type in {
            "auton_score", "auton_miss",
            "teleop_score", "teleop_miss"
        }:
            values = [{"match_number": v["match_number"], "value": parse_number(v["value"])} for v in raw_values if v["value"] is not None]

            if not values:
                continue

            game_piece = field.game_piece.name

            bucket = "auton" if stat_type.startswith("auton") else "teleop"
            numeric_values = [parse_number(v["value"]) for v in values if v["value"] is not None]

            if numeric_values:
                teams[team_number][bucket][game_piece].append({
                    "field_uuid": str(field.uuid),
                    "field_type": field.field_type,
                    "field_name": field.name,
                    "values": values,
                    "min": min(numeric_values),
                    "max": max(numeric_values),
                    "avg": mean(numeric_values)
                })

        # CAPABILITY (percentages)
        elif stat_type == "capability":
            counts = defaultdict(int)

            for v in raw_values:
                raw = v["value"]

                # Decode JSON if needed
                try:
                    decoded = json.loads(raw)
                except (TypeError, json.JSONDecodeError):
                    decoded = raw

                # If the answer is a list, count each item
                if isinstance(decoded, list):
                    for item in decoded:
                        counts[item] += 1
                else:
                    counts[decoded] += 1

            total = sum(counts.values())

            teams[team_number]["capability"].append({
                "field_uuid": str(field.uuid),
                "field_type": field.field_type,
                "field_name": field.name,
                "values": list(counts.keys()),
                "percentages": [
                    {
                        "value": val,
                        "percentage": round((count / total) * 100, 2)
                    }
                    for val, count in counts.items()
                ]
            })

        # OTHER (text / misc)
        elif stat_type == "other":
            teams[team_number]["other"].append({
                "field_uuid": str(field.uuid),
                "field_type": field.field_type,
                "field_name": field.name,
                "values": raw_values
            })

    # Convert defaultdicts to lists
    result = []
    for team in teams.values():
        team["teleop"] = dict(team["teleop"])
        team["auton"] = dict(team["auton"])
        result.append(team)

    return result

# Custom Events
@app.get("/event/custom/{season_uuid}")
async def get_custom_events(season_uuid: str):
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    return await Event.filter(season=season, custom=True)

@app.post("/event/custom/{season_uuid}/create")
async def create_custom_event(
    season_uuid: str,

    event_code: str = Form(...),
    event_name: str = Form(...),
    event_type: str = Form(...),
    event_city: str = Form(...),
    event_country: str = Form(...),
    event_start_date: str = Form(...),
    event_end_date: str = Form(...)
    
    ):
    
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    event, _ = await Event.get_or_create(
        season=season,
        event_code=event_code,
        name=event_name,
        type=event_type,
        city=event_city,
        country=event_country,
        start_date=event_start_date,
        end_date=event_end_date,
        custom=True
    )

    return event