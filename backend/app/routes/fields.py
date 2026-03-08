from typing import Any
import json
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import require_superuser
from ..models import GamePiece, MatchScoutingField, Organization, Season, User
from ..schemas.generic import MessageResponse
from ..schemas.fields import MatchScoutingFieldRequest, MatchScoutingFieldResponse, ReorderMatchScoutingFieldsRequest
from ..utils import get_season, IS_DEV


router: APIRouter = APIRouter(
    tags=["Match Scouting Fields"],
    include_in_schema=IS_DEV
)

# TODO: This needs a proper response_model
@router.get("/fields/season/{season_uuid}")
async def get_season_fields(season_uuid: UUID) -> list[Any]:
    """
    Get all match scouting fields for a season

    Parameters:
        season_uuid (`UUID`): The UUID of the season to get fields for

    Returns:
        `list[MatchScoutingField]`: A list of all match scouting fields for the season
    """
    # Find the season
    season: Season = await get_season(season_uuid)

    # Fetch all fields for the season including their children
    fields: list[MatchScoutingField] = await MatchScoutingField.filter(season=season, archived=False).prefetch_related("children")

    # Convert queryset to list of dicts
    field_list: list[MatchScoutingField] = [f for f in fields]

    # Build lookup dict for fast parent-child linking
    field_map = {f.uuid: f for f in field_list}

    # Prepare the tree structure
    tree = []

    # Attach children recursively
    for field in field_list:
        # Convert model instance to dict
        field_data = {
            "uuid": str(field.uuid),
            "name": field.name,
            "description": field.description,
            "field_type": field.field_type,
            "stat_type": field.stat_type,
            "game_piece_uuid": str(field.game_piece_id) if field.game_piece_id else None,
            "required": field.required,
            "options": field.options,
            "order": field.order,
            "organization_id": str(field.organization_id) if field.organization_id else None,
            "fields": []  # for children
        }

        # If field has a parent, attach it to parent's "fields" list
        if field.parent_id:
            parent = field_map.get(field.parent_id)
            if not hasattr(parent, "_tree_fields"):
                parent._tree_fields = []
            parent._tree_fields.append(field_data)
        else:
            # Top-level field (no parent)
            tree.append(field_data)

        # Store the built dict for later child assignment
        field._tree_data = field_data

    # Now attach children properly to their parents' dicts
    for field in field_list:
        if hasattr(field, "_tree_fields"):
            field._tree_data["fields"] = field._tree_fields

    # Sort recursively by `order`
    def sort_fields(fields):
        fields.sort(key=lambda f: f["order"])
        for f in fields:
            sort_fields(f["fields"])

    sort_fields(tree)

    return tree

@router.delete("/fields/season/{season_uuid}/clear", response_model=MessageResponse)
async def clear_season_fields(season_uuid: UUID, superuser: User = Depends(require_superuser)) -> dict[str, str]:
    """
    Clear all match scouting fields for a season

    Requires superuser access

    Parameters:
        season_uuid (`UUID`): The UUID of the season to clear fields for

    Returns:
        `MessageResponse`: A message indicating that the fields were cleared
    """
    season: Season = await get_season(season_uuid)

    await MatchScoutingField.filter(season=season).update(archived=True)
    return {"message": "Fields archived"}

@router.post("/fields/season/{season_uuid}/create", response_model=MatchScoutingFieldResponse)
async def create_season_field(
        season_uuid: UUID,
        data: MatchScoutingFieldRequest,
        superuser: User = Depends(require_superuser)
    ) -> MatchScoutingFieldResponse:
    """
    Create a new match scouting field

    Requires superuser access

    Parameters:
        season_uuid (`UUID`): The UUID of the season to create the field for
        data (MatchScoutingFieldRequest): The data to create the field

    Returns:
        `MatchScoutingField`: The created field
    """
    season: Season = await get_season(season_uuid)

    if data.stat_type == "auton_score" or data.stat_type == "auton_miss" or data.stat_type == "teleop_score" or data.stat_type == "teleop_miss":
        game_piece = await GamePiece.get_or_none(uuid=data.game_piece_uuid)
        if not game_piece:
            
            # Temporary hack to try and repair game pieces for imported fields
            # TODO: Replace this later for proper game piece repairing in the edit dialog
            game_pieces = await GamePiece.all()
            matching_game_pieces = [gp for gp in game_pieces if any(word in data.name.split() for word in gp.name.split())]
            
            if matching_game_pieces:
                print("WARNING: Game piece not found. Using closest match based on field name: " + matching_game_pieces[0].name)
                game_piece = matching_game_pieces[0]
            else:
                raise HTTPException(status_code=404, detail="Game piece not found")
    else:
        game_piece = None

    if data.organization_uuid != "" and data.organization_uuid is not None:
        organization = await Organization.get_or_none(uuid=data.organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    if data.parent_uuid != "" and data.parent_uuid is not None:
        parent = await MatchScoutingField.get_or_none(uuid=data.parent_uuid)
        if not parent:
            print("section not found", data.parent_uuid)
            raise HTTPException(status_code=404, detail="Section not found")
    else:
        parent = None        

    # When importing from a preset, uuid is provided
    if data.uuid != "" and data.uuid is not None:
        # Check if an existing archived field exists
        existing_field = await MatchScoutingField.filter(
            uuid=data.uuid,
            archived=True
        ).first()

        # If an existing archived field exists, edit it with the given data and unarchive it
        if existing_field:
            existing_field.parent = parent
            existing_field.season = season
            existing_field.name = data.name
            existing_field.description = data.description if data.description is not None else ""
            existing_field.field_type = data.field_type
            existing_field.stat_type = data.stat_type
            existing_field.game_piece = game_piece
            existing_field.required = data.required
            existing_field.options = data.options
            existing_field.order = data.order
            existing_field.organization = organization
            existing_field.archived = False
            await existing_field.save()

            field = existing_field
        
        # Otherwise, create a new one
        else:
            field = await MatchScoutingField.create(
                uuid=data.uuid,
                parent=parent,
                season=season, 
                name=data.name, 
                description=data.description,
                field_type=data.field_type, 
                stat_type=data.stat_type, 
                game_piece=game_piece, 
                required=data.required, 
                options=data.options, 
                order=data.order, 
                organization=organization
            )
    else:
        field = await MatchScoutingField.create(
            parent=parent,
            season=season, 
            name=data.name, 
            description=data.description,
            field_type=data.field_type, 
            stat_type=data.stat_type, 
            game_piece=game_piece, 
            required=data.required, 
            options=data.options, 
            order=data.order, 
            organization=organization
        )

    return MatchScoutingFieldResponse(
        uuid=field.uuid,
        season=field.season.uuid,
        name=field.name,
        description=field.description,
        field_type=field.field_type,
        stat_type=field.stat_type,
        game_piece_uuid=field.game_piece.uuid if field.game_piece else None,
        required=field.required,
        options=field.options,
        order=field.order,
        organization_uuid=field.organization.uuid if field.organization else None,
    )

@router.post("/fields/season/{season_uuid}/edit/{field_uuid}", response_model=MatchScoutingFieldResponse)
async def edit_season_field(
        season_uuid: UUID,
        field_uuid: UUID,
        data: MatchScoutingFieldRequest,
        superuser: User = Depends(require_superuser)
    ) -> MatchScoutingField:
    """
    Edit a match scouting field

    Requires superuser access

    Parameters:
        season_uuid (`UUID`): The UUID of the season to edit the field for
        field_uuid (`UUID`): The UUID of the field to edit
        data (MatchScoutingFieldRequest): The data to edit the field

    Returns:
        `MatchScoutingField`: The edited field
    """

    field = await MatchScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
        
    season: Season = await get_season(season_uuid)

    if data.stat_type == "auton_score" or data.stat_type == "auton_miss" or data.stat_type == "teleop_score" or data.stat_type == "teleop_miss":
        game_piece = await GamePiece.get_or_none(uuid=data.game_piece_uuid)
        if not game_piece:
            raise HTTPException(status_code=404, detail="Game piece not found")
    else:
        game_piece = None

    if data.organization_uuid != "" and data.organization_uuid is not None:
        organization = await Organization.get_or_none(uuid=data.organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    field.name = data.name
    field.description = data.description
    field.field_type = data.field_type
    field.stat_type = data.stat_type
    field.game_piece = game_piece
    field.required = data.required
    field.options = data.options
    field.order = data.order
    field.organization = organization
    await field.save()
    return field

@router.patch("/fields/{season_uuid}/reorder", response_model=MessageResponse)
async def move_match_scouting_fields(
        season_uuid: UUID,
        data: ReorderMatchScoutingFieldsRequest,
) -> MessageResponse:
    """
    Reorder match scouting fields for a season

    Parameters:
        season_uuid (`UUID`): The UUID of the season to reorder fields for
        data (`ReorderMatchScoutingFieldsRequest`): The data to reorder the fields

    Returns:
        `MessageResponse`: A message indicating that the fields were reordered
    """
    season: Season = await get_season(season_uuid)

    for field in data:
        if field.parent_uuid:
            parent = await MatchScoutingField.get_or_none(uuid=field.parent_uuid)
            await MatchScoutingField.filter(uuid=field.uuid, season=season).update(order=field.order, parent=parent)
        else:
            await MatchScoutingField.filter(uuid=field.uuid, season=season).update(order=field.order, parent_id=None)

    return MessageResponse(message="Fields reordered")

@router.get("/fields/get_presets")
async def get_match_scouting_field_presets(superuser: User = Depends(require_superuser)) -> list[Any]:    
    """
    Get all JSON match scouting field presets

    Requires superuser access

    Returns:
        `list[Any]`: A list of all match scouting field presets
    """
    path = Path("./app/match_scouting_presets")
    presets = []

    for file in path.iterdir():
        with open(file, "r") as f:
            presets.append({ "name": file.stem, "preset": json.load(f) })

    return presets

@router.delete("/fields/delete/{field_uuid}", response_model=MessageResponse)
async def delete_field(field_uuid: UUID, superuser: User = Depends(require_superuser)) -> dict[str, str]:
    """
    Delete a match scouting field

    Requires superuser access

    Parameters:
        field_uuid (`UUID`): The UUID of the field to delete

    Returns:
        `MessageResponse`: A message indicating that the field was deleted
    """
    field: MatchScoutingField | None = await MatchScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    
    field.archived = True
    await field.save()

    return {"message": "Field archived"}