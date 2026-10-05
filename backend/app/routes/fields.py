from uuid import UUID
from typing import Literal
import json
from collections import defaultdict
from pathlib import Path

from tortoise.transactions import in_transaction
from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import Identity, require_superuser
from ..models import ScoutingField, ScoutingType, Season
from ..schemas.generic import MessageResponse
from ..schemas.fields import FieldChoiceResponse, FieldOptionsResponse, MatchScoutingFieldRequest, MatchScoutingFieldResponse, PitScoutingFieldRequest, PitScoutingFieldResponse, ScoutingFieldPresetResponse
from ..utils import get_season, IS_DEV


router: APIRouter = APIRouter(
    tags=["Scouting Fields"],
    include_in_schema=IS_DEV
)

# Helper Functions
def construct_options_from_field(field: ScoutingField) -> FieldOptionsResponse | None:
    """
    Construct a FieldOptionsResponse from a MatchScoutingField or PitScoutingField

    Parameters:
        field (`ScoutingField`): The field to construct the options from

    Returns:
        `FieldOptionsResponse | None`: The constructed options, or None if the field has no options
    """
    if not field.options:
        return None

    choices: list[FieldChoiceResponse] | None = None

    if field.options.choices:
        choices = [
            FieldChoiceResponse(
                uuid=choice.uuid,
                name=choice.name,
                simple_name=choice.simple_name,
                created_at=choice.created_at
            ) for choice in field.options.choices
        ]

    return FieldOptionsResponse(
        uuid=field.options.uuid,
        default=field.options.default,
        minimum=field.options.minimum,
        maximum=field.options.maximum,
        choices=choices,
        created_at=field.options.created_at
    )

def construct_field_response(field: ScoutingField) -> MatchScoutingFieldResponse | PitScoutingFieldResponse:
    """
    Construct a MatchScoutingFieldResponse or PitScoutingFieldResponse from a ScoutingField

    Parameters:
        field (`ScoutingField`): The field to construct the response from

    Returns:
        `MatchScoutingFieldResponse | PitScoutingFieldResponse`: The constructed response
    """
    match field.scouting_type:
        case ScoutingType.MATCH:
            return MatchScoutingFieldResponse(
                uuid=field.uuid,
                season_uuid=field.season.uuid if field.season else None,
                organization_uuid=field.organization.uuid if field.organization else None,
                parent_uuid=field.parent.uuid if field.parent else None,
                name=field.name,
                description=field.description,
                scouting_type=ScoutingType.MATCH,
                field_type=field.field_type,
                stat_type=field.stat_type,
                game_piece_uuid=field.game_piece.uuid if field.game_piece else None,
                required=field.required,
                options=construct_options_from_field(field),
                order=field.order,
                archived=field.archived,
                created_at=field.created_at
            )

        case ScoutingType.PIT:
            return PitScoutingFieldResponse(
                uuid=field.uuid,
                season_uuid=field.season.uuid if field.season else None,
                organization_uuid=field.organization.uuid if field.organization else None,
                name=field.name,
                description=field.description,
                scouting_type=ScoutingType.PIT,
                field_type=field.field_type,
                required=field.required,
                options=construct_options_from_field(field),
                order=field.order,
                archived=field.archived,
                created_at=field.created_at
            )

# Routes
@router.get("/fields/season/{season_uuid}/{scouting_type}", response_model=list[MatchScoutingFieldResponse | PitScoutingFieldResponse])
async def get_season_fields(season_uuid: UUID, scouting_type: ScoutingType) -> list[MatchScoutingFieldResponse | PitScoutingFieldResponse]:
    """
    Get all scouting fields for a season. Takes season uuid and the field type.

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get fields for
        scouting_type (`ScoutingType`): The scouting type to get fields for

    Returns:
        list[MatchScoutingFieldResponse | PitScoutingFieldResponse]: A list of all scouting fields for the season
    """
    season: Season = await get_season(season_uuid)
    
    fields: list[ScoutingField] = await ScoutingField.filter(season=season, archived=False, scouting_type=scouting_type)

    returned_fields: list[MatchScoutingFieldResponse | PitScoutingFieldResponse] = []
    
    for field in fields:
        returned_fields.append(construct_field_response(field))

    return returned_fields


@router.delete("/fields/season/{season_uuid}/{scouting_type}/archive", response_model=MessageResponse)
async def archive_season_fields(season_uuid: UUID, scouting_type: ScoutingType, identity: Identity = Depends(require_superuser)) -> MessageResponse:
    """
    Archive all scouting fields for a season

    Requires superuser access

    Parameters:
        season_uuid (`UUID`): The UUID of the season to archive fields for
        scouting_type (`ScoutingType`): The scouting type to archive fields for

    Returns:
        `MessageResponse`: A message indicating that the fields were archived
    """
    season: Season = await get_season(season_uuid)

    _ = await ScoutingField.filter(season=season, scouting_type=scouting_type).update(archived=True)
    return MessageResponse(message="Fields archived")

@router.post("/fields/create", response_model=MatchScoutingFieldResponse | PitScoutingFieldResponse)
async def create_field(data: MatchScoutingFieldRequest | PitScoutingFieldRequest, identity: Identity = Depends(require_superuser)) -> MatchScoutingFieldResponse | PitScoutingFieldResponse:
    """
    Create a new scouting field

    Parameters:
        data (`MatchScoutingFieldRequest | PitScoutingFieldRequest`): The data to create the field with

    Returns:
        `MatchScoutingFieldResponse | PitScoutingFieldResponse`: The created field

    TODO: Allow non-superusers to create organization fields
    """
    season: Season = await get_season(data.season_uuid)

    field: ScoutingField = await ScoutingField.create(
        uuid=data.uuid,
        season=season,
        organization=data.organization_uuid,
        name=data.name,
        description=data.description,
        scouting_type=data.scouting_type,
        field_type=data.field_type,
        required=data.required,
        options=data.options,
        order=data.order,
        archived=data.archived,
        created_by=identity.session
    )

    match data.scouting_type:
        case ScoutingType.MATCH:
            field.parent_id = data.parent_uuid
            field.stat_type = data.stat_type
            field.game_piece_id = data.game_piece_uuid
            await field.save()

            return construct_field_response(field)
        case ScoutingType.PIT:
            return construct_field_response(field)

@router.patch("/fields/edit", response_model=MatchScoutingFieldResponse | PitScoutingFieldResponse)
async def edit_field(data: MatchScoutingFieldRequest | PitScoutingFieldRequest) -> MatchScoutingFieldResponse | PitScoutingFieldResponse:
    """
    Edit a scouting field

    Parameters:
        data (`MatchScoutingFieldRequest | PitScoutingFieldRequest`): The data to edit the field

    Returns:
        `MatchScoutingFieldResponse | PitScoutingFieldResponse`: The edited field
    """
    field: ScoutingField | None = await ScoutingField.get_or_none(uuid=data.uuid)

    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    field.update_from_dict(data.model_dump(exclude_unset=True))
    
    await field.save()

    return construct_field_response(field)

@router.get("/fields/presets/{scouting_type}", response_model=list[ScoutingFieldPresetResponse])
async def get_field_presets(scouting_type: ScoutingType) -> list[ScoutingFieldPresetResponse]:
    """
    Get all scouting field presets

    Parameters:
        scouting_type (`ScoutingType`): The scouting type to get presets for

    Returns:
        `list[ScoutingFieldPresetResponse]`: A list of all scouting field presets
    """
    presets: list[ScoutingFieldPresetResponse] = []

    match scouting_type:
        case ScoutingType.MATCH:
            path = Path("./app/match_scouting_presets")
        case ScoutingType.PIT:
            path = Path("./app/pit_scouting_presets")

    for file in path.iterdir():
        with open(file, "r") as f:
            presets.append(ScoutingFieldPresetResponse(
                name=file.stem,
                preset=json.load(f)
            ))

    return presets

@router.delete("/fields/archive/{field_uuid}", response_model=MessageResponse)
async def archive_field(field_uuid: UUID, identity: Identity = Depends(require_superuser)):
    """
    Archive a scouting field

    Requires superuser access

    Parameters:
        field_uuid (`UUID`): The UUID of the field to archive

    Returns:
        `MessageResponse`: A message indicating that the field was archived

    TODO: Allow non-superusers to archive organization fields that belong to their organization
    """
    field: ScoutingField | None = await ScoutingField.get_or_none(uuid=field_uuid)

    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    await field.delete()
    return MessageResponse(message="Field archived")

@router.patch("/fields/reorder", response_model=list[MatchScoutingFieldResponse | PitScoutingFieldResponse])
async def reorder_fields(data: list[MatchScoutingFieldRequest] | list[PitScoutingFieldRequest], identity: Identity = Depends(require_superuser)) -> list[MatchScoutingFieldResponse | PitScoutingFieldResponse]:
    """
    Reorder scouting fields

    Based on the order of the fields in the request, the fields will be reordered to that order.
    It is assumed that all fields in this request are meant to be reordered together. Only pass fields to this request that you want to reorder.
    If fields have parents, the parents must be in the request as well. Order children on a different "level" than their parents, but in the order they appear in the list.

    Parameters:
        data (`list[MatchScoutingFieldRequest] | list[PitScoutingFieldRequest]`): The data to reorder the fields

    Returns:
        `list[MatchScoutingFieldResponse | PitScoutingFieldResponse]`: A list of all fields in the new order

    TODO: Allow non-superusers to reorder organization fields that belong to their organization
    """
    # Ensure all fields have the same scouting type
    scouting_type: Literal[ScoutingType.MATCH, ScoutingType.PIT] = data[0].scouting_type

    if any(field.scouting_type != scouting_type for field in data):
        raise HTTPException(
            status_code=400,
            detail="All fields in a reorder request must have the same scouting type.",
        )

    # Ensure UUIDs are unique
    field_uuids: list[UUID] = [field.uuid for field in data]
    if len(field_uuids) != len(set(field_uuids)):
        raise HTTPException(
            status_code=400,
            detail="A field may only appear once in a reorder request.",
        )

    fields: list[ScoutingField] = await ScoutingField.filter(
        uuid__in=field_uuids,
        scouting_type=scouting_type,
    ).prefetch_related(
        "parent",
        "season",
        "organization",
        "game_piece",
        "options",
    )

    # Ensure all fields were found on the server
    fields_by_uuid: dict[UUID, ScoutingField] = {field.uuid: field for field in fields}
    missing: list[UUID] = [
        uuid
        for uuid in field_uuids
        if uuid not in fields_by_uuid
    ]

    if missing:
        raise HTTPException(
            status_code=404,
            detail=f"One or more fields were not found: {missing}",
        )

    # Ensure all parents are in the request
    requested_uuids: set[UUID] = set[UUID](field_uuids)
    for field in fields:
        if field.parent_id is not None and field.parent_id not in requested_uuids:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Field {field.uuid} has parent {field.parent_id}, "
                    "but that parent was not included in the reorder request."
                ),
            )

    # Calculate the new order for each field
    next_order: defaultdict[object, int] = defaultdict[object, int](int)

    for request_field in data:
        field: ScoutingField = fields_by_uuid[request_field.uuid]

        parent_id = field.parent_id

        field.order = next_order[parent_id]
        next_order[parent_id] += 1

    # Update fields
    async with in_transaction():
        _ = await ScoutingField.bulk_update(
            fields,
            fields=["order"],
        )

    ordered_fields = [
        fields_by_uuid[uuid]
        for uuid in field_uuids
    ]

    return [
        construct_field_response(field)
        for field in ordered_fields
    ]