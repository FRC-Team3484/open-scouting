from backend.app.models import Season


from fastapi import APIRouter, HTTPException

from ..models import Event, Season
from ..schemas.event import CustomEventsRequest, EventResponse, CustomEventRequest
from ..utils import get_season

router: APIRouter = APIRouter()

@router.get("/event/custom/{season_uuid}", response_model=list[EventResponse])
async def get_custom_events(data: CustomEventsRequest) -> list[Event]:
    season: Season = await get_season(data.season_uuid)

    return await Event.filter(season=season, custom=True)

@router.post("/event/custom/{season_uuid}/create", response_model=EventResponse)
async def create_custom_event(
        data: CustomEventRequest
    ) -> Event:
    
    season: Season = await get_season(data.season_uuid)

    event, _ = await Event.get_or_create(
        season=season,
        event_code=data.event_code,
        name=data.event_name,
        type=data.event_type,
        city=data.event_city,
        country=data.event_country,
        start_date=data.event_start_date,
        end_date=data.event_end_date,
        custom=True
    )

    return event