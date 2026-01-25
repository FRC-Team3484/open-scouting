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

from .models import \
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

from .auth import get_password_hash, verify_password, create_access_token, decode_access_token
from .dependencies import get_current_user

from .routes import auth, organizations, seasons, gamepieces, fields, match_scouting, pit_scouting, data, event

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

app.include_router(auth.router)
app.include_router(organizations.router)
app.include_router(seasons.router)
app.include_router(gamepieces.router)
app.include_router(fields.router)
app.include_router(match_scouting.router)
app.include_router(pit_scouting.router)
app.include_router(data.router)
app.include_router(event.router)

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

# Routes
#    Auth


#    Organizations


#    Seasons


#    Game Pieces


#    Match Scouting Fields


#    Match Scouting Answers


#    Pit Scouting


#    Data View


# Custom Events
