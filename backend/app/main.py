import json
import os
from time import strftime
import uuid
from dotenv import load_dotenv
import requests

from fastapi import FastAPI, Form, Depends, HTTPException, status, Body
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
app = FastAPI()

# TODO: Handle production environment variables
load_dotenv(".env.development")

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

    user = await User.get_or_none(uuid=user_uuid)
    if not user:
        user = None # Sets the user to none if not a user. This should probably be the user's username later

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
            value=value,
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
    if not event.pits_generated and TBA_API_KEY != "" and TBA_API_KEY is not None:
        event_key = str(season.year) + event_code
        response = requests.get(f"https://www.thebluealliance.com/api/v3/event/{event_key}/teams", headers={"X-TBA-Auth-Key": TBA_API_KEY})
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