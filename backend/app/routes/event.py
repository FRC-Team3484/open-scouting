from fastapi import APIRouter, HTTPException

from ..models import Event, Season
from ..schemas.event import CustomEventsRequest, EventResponse, CustomEventRequest

router: APIRouter = APIRouter()

@router.get("/event/custom/{season_uuid}", response_model=list[EventResponse])
async def get_custom_events(data: CustomEventsRequest) -> list[Event]:
    season: Season | None = await Season.get_or_none(uuid=data.season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    return await Event.filter(season=season, custom=True)

@router.post("/event/custom/{season_uuid}/create", response_model=EventResponse)
async def create_custom_event(
        data: CustomEventRequest
    ) -> Event:
    
    season: Season | None = await Season.get_or_none(uuid=data.season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

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