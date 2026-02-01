import json
import os
from uuid import UUID
import httpx

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import require_superuser
from ..models import Event, Organization, PitScoutingAnswer, PitScoutingField, Season, TeamPit, User
from ..schemas.generic import MessageResponse
from ..schemas.pit_scouting import EditPitFieldRequest, PitFieldsRequest, PitFieldResponse, CreatePitFieldRequest, DeletePitFieldRequest, GetPitsForSeasonRequest, SubmitPitFieldAnswerRequest
from ..utils import get_season

router: APIRouter = APIRouter(
    tags=["Pit Scouting"],
)

TBA_API_KEY = os.getenv("TBA_API_KEY")

@router.get("/pits/fields/{season_uuid}", response_model=list[PitFieldResponse])
async def get_pit_fields(season_uuid: UUID) -> list[PitFieldResponse]:
    """
    Get all pit scouting fields for a season

    Parameters:
        data (`PitFieldsRequest`): The UUID of the season to get fields for

    Returns:
        list[PitFieldResponse]: A list of all pit scouting fields for the season
    """
    season: Season = await get_season(season_uuid)

    fields: list[PitScoutingField] = await PitScoutingField.filter(season=season)

    return [
        PitFieldResponse(
            uuid=field.uuid,
            season=season.uuid,
            name=field.name,
            field_type=field.field_type,
            options=field.options,
            order=field.order,
            organization=field.organization.uuid if field.organization else None,
            created_at=field.created_at
        ) for field in fields
    ]

@router.delete("/pits/fields/{season_uuid}/clear", response_model=MessageResponse)
async def clear_pit_fields(data: PitFieldsRequest, superuser: User = Depends(require_superuser)):
    """
    Clear all pit scouting fields for a season

    Requires superuser access

    Parameters:
        data (`PitFieldsRequest`): The UUID of the season to clear fields for

    Returns:
        `MessageResponse`: A message indicating that the fields were cleared
    """
    season: Season = await get_season(data.season_uuid)

    await PitScoutingField.filter(season=season).delete()
    return {"message": "Fields cleared"}

@router.post("/pits/fields/{season_uuid}/create", response_model=PitFieldResponse)
async def create_pit_field(
        data: CreatePitFieldRequest,
        superuser: User = Depends(require_superuser)
    ) -> PitFieldResponse:
    """
    Create a new pit scouting field

    Requires superuser access

    Parameters:
        data (`CreatePitFieldRequest`): The data to create the field

    Returns:
        `PitFieldResponse`: The created field
    """

    season: Season = await get_season(data.season_uuid)

    if data.organization_uuid != "":
        organization: Organization | None = await Organization.get_or_none(uuid=data.organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    field: PitScoutingField = await PitScoutingField.create(
        season=season,
        name=data.name,
        field_type=data.field_type,
        options=data.options,
        order=data.order,
        organization=organization
    )

    return PitFieldResponse(
        uuid=field.uuid,
        season=season.uuid,
        name=field.name,
        field_type=field.field_type,
        options=field.options,
        order=field.order,
        organization=field.organization.uuid if field.organization else None,
        created_at=field.created_at
    )

@router.patch("/pits/fields/{season_uuid}/edit/{field_uuid}", response_model=PitFieldResponse)
async def edit_pit_field(
        data: EditPitFieldRequest,
        superuser: User = Depends(require_superuser)
    ) -> PitFieldResponse:
    """
    Edit a pit scouting field

    Requires superuser access

    Parameters:
        data (`EditPitFieldRequest`): The data to edit the field

    Returns:
        `PitFieldResponse`: The edited field
    """
    
    season: Season = await get_season(data.season_uuid)

    field: PitScoutingField | None = await PitScoutingField.get_or_none(uuid=data.field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    if data.organization_uuid != "":
        organization: Organization | None = await Organization.get_or_none(uuid=data.organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    field.name = data.name
    field.field_type = data.field_type
    field.options = data.options
    field.order = data.order
    field.organization = organization

    await field.save()

    return PitFieldResponse(
        uuid=field.uuid,
        season=season.uuid,
        name=field.name,
        field_type=field.field_type,
        options=field.options,
        order=field.order,
        organization=field.organization.uuid if field.organization else None,
        created_at=field.created_at
    )

@router.delete("/pits/fields/{field_uuid}/delete", response_model=PitFieldResponse)
async def delete_pit_field(
        data: DeletePitFieldRequest,
        superuser: User = Depends(require_superuser)
    ) -> PitFieldResponse:
    """
    Delete a pit scouting field

    Requires superuser access

    Parameters:
        data (`DeletePitFieldRequest`): The UUID of the field to delete

    Returns:
        `PitFieldResponse`: The deleted field
    """

    field: PitScoutingField | None = await PitScoutingField.get_or_none(uuid=data.field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    await field.delete()

    return PitFieldResponse(
        uuid=field.uuid,
        season=season.uuid,
        name=field.name,
        field_type=field.field_type,
        options=field.options,
        order=field.order,
        organization=field.organization.uuid if field.organization else None,
        created_at=field.created_at
    )

# TODO: This needs a proper response_model
@router.post("/pits/get/{season_uuid}")
async def get_pits(
        data: GetPitsForSeasonRequest
    ):
    """
    Get all pits for a season

    Parameters:
        data (`GetPitsForSeasonRequest`): The UUID of the season to get pits for

    Returns:
        list: A list of all pits for the season
    """
    season: Season = await get_season(data.season_uuid)

    event, _ = await Event.get_or_create(
        season=season,
        event_code=data.event_code,
        name=data.event_name,
        type=data.event_type,
        city=data.event_city,
        country=data.event_country,
        start_date=data.event_start_date,
        end_date=data.event_end_date
    )

    # If pits have not been generated yet, get teams from TBA and create TeamPits
    if not event.pits_generated and TBA_API_KEY != "" and TBA_API_KEY is not None and event.custom is False:
        event_key = str(season.year) + data.event_code
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

@router.post("/pits/submit/{season_uuid}/{team_number}", response_model=MessageResponse)
async def submit_pit(
        data: SubmitPitFieldAnswerRequest
    ):
    """
    Get the season and event from the uuids. Then, check if a pit with that team number exists.
    If it does, update that pit

    For the answers in that pit, find each answer that does not already exist on the server, and add them

    If a pit does not exist, that means it was created by the client of a user. It should be created.

    Parameters:
        data (`SubmitPitFieldAnswerRequest`): The UUID of the season and event to get pits for

    Returns:
        MessageResponse: A message indicating that the pits were submitted
    """
    
    season: Season = await get_season(data.season_uuid)

    event = await Event.get_or_none(event_code=data.event_code, season=season).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    pit, created = await TeamPit.get_or_create(
        team_number=data.team_number,
        season=season,
        event=event,
        nickname=data.nickname
    )

    if created:
        print("Created pit", pit.uuid, "for team", data.team_number, "and event", event.uuid)

    for answer in json.loads(data.answers):
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

    return {"message": "Pit submitted successfully"}