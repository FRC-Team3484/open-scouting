import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from .routes import auth, organizations, seasons, gamepieces, fields, match_scouting, pit_scouting, data, event

# Setup
app: FastAPI = FastAPI(root_path="/api")

load_dotenv()
ENV = os.getenv("ENV", "development")

origins = os.getenv("CORS_ORIGINS", "*").split(",")
TBA_API_KEY = os.getenv("TBA_API_KEY")

if TBA_API_KEY is None or TBA_API_KEY == "":
    print("TBA_API_KEY is not set. Pit scouting will not work as expected.")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create routes
app.include_router(auth.router)
app.include_router(organizations.router)
app.include_router(seasons.router)
app.include_router(gamepieces.router)
app.include_router(fields.router)
app.include_router(match_scouting.router)
app.include_router(pit_scouting.router)
app.include_router(data.router)
app.include_router(event.router)

# Setup database
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