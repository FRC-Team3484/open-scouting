from collections import defaultdict
from datetime import datetime
import json
import os
from pathlib import Path
from typing import Any
from uuid import UUID
import httpx

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import require_superuser
from ..models import Event, Organization, PitScoutingAnswer, PitScoutingField, Season, TeamPit, User
from ..schemas.generic import MessageResponse
from ..schemas.pit_scouting import AdminPitResponse, PitFieldResponse, PitFieldRequest, GetPitsForSeasonRequest, ReorderPitFieldsRequest, SubmitPitFieldAnswerRequest
from ..utils import get_season, IS_DEV

router: APIRouter = APIRouter(
    tags=["Pit Scouting"],
    include_in_schema=IS_DEV
)

TBA_API_KEY = os.getenv("TBA_API_KEY")

def to_date_string(value: str) -> str:
    try:
        dt = datetime.fromisoformat(value)
    except ValueError:
        dt = datetime.strptime(value, "%Y-%m-%d")

    return dt.date().isoformat()

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

    fields: list[PitScoutingField] = await PitScoutingField.filter(season=season, archived=False)

    return [
        PitFieldResponse(
            uuid=field.uuid,
            season=season.uuid,
            name=field.name,
            description=field.description,
            required=field.required,
            field_type=field.field_type,
            options=field.options,
            order=field.order,
            organization=field.organization.uuid if field.organization else None,
            created_at=field.created_at
        ) for field in fields
    ]

@router.delete("/pits/fields/{season_uuid}/clear", response_model=MessageResponse)
async def clear_pit_fields(season_uuid: UUID, superuser: User = Depends(require_superuser)):
    """
    Clear all pit scouting fields for a season

    Requires superuser access

    Parameters:
        season_uuid (`UUID`): The UUID of the season to clear fields for
        data (`PitFieldsRequest`): The UUID of the season to clear fields for

    Returns:
        `MessageResponse`: A message indicating that the fields were cleared
    """
    season: Season = await get_season(season_uuid)

    await PitScoutingField.filter(season=season).update(archived=True)
    return {"message": "Fields cleared"}

@router.post("/pits/fields/{season_uuid}/create", response_model=PitFieldResponse)
async def create_pit_field(
        season_uuid: UUID,
        data: PitFieldRequest,
        superuser: User = Depends(require_superuser)
    ) -> PitFieldResponse:
    """
    Create a new pit scouting field

    Requires superuser access

    Parameters:
        season_uuid (`UUID`): The UUID of the season to create the field for
        data (`CreatePitFieldRequest`): The data to create the field

    Returns:
        `PitFieldResponse`: The created field
    """
    season: Season = await get_season(season_uuid)

    if data.organization_uuid != "" and data.organization_uuid is not None:
        organization: Organization | None = await Organization.get_or_none(uuid=data.organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    # When importing from a preset, uuid is provided
    if data.uuid != "" and data.uuid is not None:
        # Check if an existing archived field exists
        existing_field = await PitScoutingField.filter(
            uuid=data.uuid, 
            archived=True
        ).first()

        # If an existing archived field exists, edit it with the given data and unarchive it
        if existing_field:
            existing_field.season = season
            existing_field.name = data.name
            existing_field.description = data.description
            existing_field.required = data.required
            existing_field.field_type = data.field_type
            existing_field.options = data.options
            existing_field.order = data.order
            existing_field.organization = organization
            existing_field.archived = False
            await existing_field.save()

            field = existing_field

        # Otherwise, create a new one
        else:
            field: PitScoutingField = await PitScoutingField.create(
                uuid=data.uuid,
                season=season,
                name=data.name,
                description=data.description,
                required=data.required,
                field_type=data.field_type,
                options=data.options,
                order=data.order,
                organization=organization
            )

    else:
        # Otherwise, create a new field
        field: PitScoutingField = await PitScoutingField.create(
            season=season,
            name=data.name,
            description=data.description,
            required=data.required,
            field_type=data.field_type,
            options=data.options,
            order=data.order,
            organization=organization
        )
        

    return PitFieldResponse(
        uuid=field.uuid,
        season=season.uuid,
        name=field.name,
        description=field.description,
        required=field.required,
        field_type=field.field_type,
        options=field.options,
        order=field.order,
        organization=field.organization.uuid if field.organization else None,
        created_at=field.created_at
    )

@router.patch("/pits/fields/{season_uuid}/edit/{field_uuid}", response_model=PitFieldResponse)
async def edit_pit_field(
        season_uuid: UUID,
        field_uuid: UUID,
        data: PitFieldRequest,
        superuser: User = Depends(require_superuser)
    ) -> PitFieldResponse:
    """
    Edit a pit scouting field

    Requires superuser access

    Parameters:
        season_uuid (`UUID`): The UUID of the season to edit the field for
        field_uuid (`UUID`): The UUID of the field to edit
        data (`PitFieldRequest`): The data to edit the field

    Returns:
        `PitFieldResponse`: The edited field
    """
    
    season: Season = await get_season(season_uuid)

    field: PitScoutingField | None = await PitScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    if data.organization_uuid != "" and data.organization_uuid is not None:
        organization: Organization | None = await Organization.get_or_none(uuid=data.organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    field.name = data.name
    field.description = data.description
    field.required = data.required
    field.field_type = data.field_type
    field.options = data.options
    field.order = data.order
    field.organization = organization

    await field.save()

    return PitFieldResponse(
        uuid=field.uuid,
        season=season.uuid,
        name=field.name,
        description=field.description,
        required=field.required,
        field_type=field.field_type,
        options=field.options,
        order=field.order,
        organization=field.organization.uuid if field.organization else None,
        created_at=field.created_at
    )

@router.patch("/pits/fields/{season_uuid}/reorder", response_model=MessageResponse)
async def move_pit_fields(
        season_uuid: UUID,
        data: ReorderPitFieldsRequest,
) -> MessageResponse:
    """
    Reorder pit scouting fields for a season

    Parameters:
        season_uuid (`UUID`): The UUID of the season to reorder fields for
        data (`ReorderPitFieldsRequest`): The data to reorder the fields

    Returns:
        `MessageResponse`: A message indicating that the fields were reordered
    """

    season: Season = await get_season(season_uuid)

    for field in data:
        await PitScoutingField.filter(uuid=field.uuid, season=season).update(order=field.order)

    return MessageResponse(message="Fields reordered")

@router.delete("/pits/fields/{field_uuid}/delete", response_model=MessageResponse)
async def delete_pit_field(
        field_uuid: UUID,
        superuser: User = Depends(require_superuser)
    ) -> MessageResponse:
    """
    Delete a pit scouting field

    Requires superuser access

    Parameters:
        field_uuid (`UUID`): The UUID of the field to delete
        data (`DeletePitFieldRequest`): The UUID of the field to delete

    Returns:
        `MessageResponse`: A message indicating that the field was deleted
    """

    field: PitScoutingField | None = await PitScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    field.archived = True
    await field.save()

    return MessageResponse(message="Field deleted")

# TODO: This needs a proper response_model
@router.post("/pits/get/{season_uuid}")
async def get_pits(
        season_uuid: UUID,
        data: GetPitsForSeasonRequest
    ):
    """
    Get all pits for a season

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get pits for
        data (`GetPitsForSeasonRequest`): The UUID of the season to get pits for

    Returns:
        list: A list of all pits for the season
    """
    season: Season = await get_season(season_uuid)

    event, _ = await Event.get_or_create(
        season=season,
        event_code=data.event_code,
        name=data.event_name,
        type=data.event_type,
        city=data.event_city,
        country=data.event_country,
        start_date=to_date_string(data.event_start_date),
        end_date=to_date_string(data.event_end_date),
        custom=data.event_custom
    )

    # If pits have not been generated yet, get teams from TBA and create TeamPits
    if not event.pits_generated and TBA_API_KEY != "" and TBA_API_KEY is not None and event.custom == False:
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
        season_uuid: UUID,
        team_number: int,
        data: SubmitPitFieldAnswerRequest
    ):
    """
    Get the season and event from the uuids. Then, check if a pit with that team number exists.
    If it does, update that pit

    For the answers in that pit, find each answer that does not already exist on the server, and add them

    If a pit does not exist, that means it was created by the client of a user. It should be created.

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get pits for
        team_number (`int`): The team number to get pits for
        data (`SubmitPitFieldAnswerRequest`): The UUID of the season and event to get pits for

    Returns:
        MessageResponse: A message indicating that the pits were submitted
    """
    
    season: Season = await get_season(season_uuid)

    event = await Event.get_or_none(event_code=data.event_code, season=season).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    pit, created = await TeamPit.get_or_create(
        uuid=data.uuid,
        team_number=team_number,
        season=season,
        event=event,
        nickname=data.nickname
    )

    if created:
        print("Created pit", pit.uuid, "for team", team_number, "and event", event.uuid)

    for answer in data.answers:
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

@router.get("/pits/get", response_model=list[AdminPitResponse])
async def get_all_pits(superuser = Depends(require_superuser)) -> list[AdminPitResponse]:
    """
    Get all pits

    Requires superuser access

    Returns:
        list[AdminPitResponse]: A list of all pits
    """
    answers = defaultdict(int)

    for pit_id in await PitScoutingAnswer.all().values_list(
        "team_id", flat=True
    ):
        answers[pit_id] += 1

    return [
        AdminPitResponse(
            uuid=pit.uuid, 
            event_name=pit.event.name,
            event_code=pit.event.event_code,
            team_number=pit.team_number, 
            answers=answers[pit.uuid],
            created_at=pit.created_at
        ) for pit in await TeamPit.all().select_related("event")
    ]

@router.delete("/pits/delete/{pit_uuid}", response_model=MessageResponse)
async def delete_pit(pit_uuid: UUID, superuser = Depends(require_superuser)) -> MessageResponse:
    """
    Delete a pit

    Requires superuser access

    Parameters:
        pit_uuid (`UUID`): The UUID of the pit to delete

    Returns:
        MessageResponse: A message indicating that the pit was deleted
    """
    await TeamPit.filter(uuid=pit_uuid).delete()
    return MessageResponse(message="Pit deleted")

@router.get("/pits/get_presets")
async def get_pit_scouting_field_presets(superuser: User = Depends(require_superuser)) -> list[Any]:    
    """
    Get all JSON pit scouting field presets

    Requires superuser access

    Returns:
        `list[Any]`: A list of all pit scouting field presets
    """
    path = Path("./app/pit_scouting_presets")
    presets = []

    for file in path.iterdir():
        with open(file, "r") as f:
            presets.append({ "name": file.stem, "preset": json.load(f) })

    return presets