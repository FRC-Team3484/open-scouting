from uuid import UUID
from fastapi import APIRouter

from ..models import Event, Season
from ..schemas.event import EventResponse, CustomEventRequest
from ..utils import get_season

router: APIRouter = APIRouter(
    tags=["Events"],
)

@router.get("/event/custom/{season_uuid}", response_model=list[EventResponse])
async def get_custom_events(season_uuid: str) -> list[EventResponse]:
    """
    Get all custom events for a season

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get custom events for

    Returns:
        list[EventResponse]: A list of all custom events for the season
    """
    season: Season = await get_season(season_uuid)

    return [
        EventResponse(
            uuid=event.uuid,
            season=season.uuid,
            event_code=event.event_code,
            name=event.name,
            type=event.type,
            city=event.city,
            country=event.country,
            start_date=event.start_date,
            end_date=event.end_date,
            pits_generated=event.pits_generated,
            custom=event.custom,
            created_at=event.created_at
        ) for event in await Event.filter(season=season, custom=True)
    ]

@router.post("/event/custom/{season_uuid}/create", response_model=EventResponse)
async def create_custom_event(
        season_uuid: UUID,
        data: CustomEventRequest
    ) -> EventResponse:
    """
    Create a custom event for a season

    Parameters:
        season_uuid (`UUID`): The UUID of the season to create a custom event for
        data (`CustomEventRequest`): The UUID of the season to create a custom event for

    Returns:
        EventResponse: The created custom event
    """
    
    season: Season = await get_season(season_uuid)

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

    return EventResponse(
        uuid=event.uuid,
        season=season.uuid,
        event_code=event.event_code,
        name=event.name,
        type=event.type,
        city=event.city,
        country=event.country,
        start_date=event.start_date,
        end_date=event.end_date,
        pits_generated=event.pits_generated,
        custom=event.custom,
        created_at=event.created_at
    )