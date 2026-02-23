import os
from uuid import UUID

from dotenv import load_dotenv
from fastapi import HTTPException

from .models import Season

load_dotenv()

MODE: str = os.getenv("PUBLIC_MODE", "prod")
IS_DEV: bool = MODE == "dev"


async def get_season(season_uuid: UUID | None = None, year: int | None = None) -> Season:
    """
    Returns the season from the db by it's UUID. Raises an exception if the season is not found

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get

    Returns:
        `Season`: The season from the db
    """
    season: Season | None = None

    if year:
        season = await Season.get_or_none(year=year)
    elif season_uuid:
        season = await Season.get_or_none(uuid=season_uuid)
    else:
        season = None

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season