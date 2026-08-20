import os
from uuid import UUID

from dotenv import load_dotenv
from fastapi import HTTPException
import httpx

from .models import Event, Season

load_dotenv()

MODE: str = os.getenv("PUBLIC_MODE", "prod")
TBA_API_KEY = os.getenv("TBA_API_KEY")
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

async def get_event(event_code: str) -> Event | None:
    """
    Given an event code, returns the event from the database. 
    
    If it cannot be found, look up event information from TBA, and create it in the database.

    Parameters:
        event_code (`str`): The event code to look up

    Returns:
        `Event`: The event from the database
    """
    event = await Event.get_or_none(event_code=event_code)

    if event is None and TBA_API_KEY != "" and TBA_API_KEY is not None:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                f"https://www.thebluealliance.com/api/v3/event/{event_code}",
                headers={"X-TBA-Auth-Key": TBA_API_KEY},
            )
        
        if response.status_code == 200:
            data = response.json()
            season = await Season.get_or_none(year=int(data["year"]))

            if season is None:
                raise HTTPException(status_code=404, detail="Season not found")

            event, _ = await Event.get_or_create(
                season=season,
                event_code=event_code,
                name=data["name"],
                type=data["event_type_string"],
                city=data["city"],
                country=data["country"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                pits_generated=False,
                custom=False,
            )
        else:
            print(f"Failed to get event ({event_code}) from TBA: {response.status_code}")
            return None

    elif event is None:
        print(f"Failed to get event ({event_code}) from database")
        return None

    return event