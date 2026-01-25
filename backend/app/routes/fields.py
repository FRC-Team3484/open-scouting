import json
import os
from pathlib import Path
from fastapi import APIRouter, Depends, Form, HTTPException

from ..dependencies import get_current_user
from ..models import GamePiece, MatchScoutingField, Organization, Season, User


router: APIRouter = APIRouter()

@router.get("/fields/season/{season_uuid}")
async def get_season_fields(season_uuid: str):
    # Find the season
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    # Fetch all fields for the season including their children
    fields = await MatchScoutingField.filter(season=season).prefetch_related("children")

    # Convert queryset to list of dicts
    field_list = [f for f in fields]

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
            "field_type": field.field_type,
            "stat_type": field.stat_type,
            "game_piece_id": str(field.game_piece_id) if field.game_piece_id else None,
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

@router.delete("/fields/season/{season_uuid}/clear")
async def clear_season_fields(season_uuid: str, current_user: User = Depends(get_current_user)):
    season = await Season.get_or_none(uuid=season_uuid)

    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    await MatchScoutingField.filter(season=season).delete()
    return {"message": "Fields cleared"}

@router.post("/fields/season/{season_uuid}/create")
async def create_season_field(
        season_uuid: str, 
        name: str = Form(...), 
        field_type: str = Form(...), 
        stat_type: str = Form(...), 
        game_piece_uuid: str = Form(...), 
        required: bool = Form(...), 
        options: list = Form(...),
        order: int = Form(...), 
        organization_uuid: str = Form(...), 
        parent_uuid: str = Form(...), 
        current_user: User = Depends(get_current_user)
    ):

    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    if stat_type == "auton_score" or stat_type == "auton_miss" or stat_type == "teleop_score" or stat_type == "teleop_miss":
        game_piece = await GamePiece.get_or_none(uuid=game_piece_uuid)
        if not game_piece:
            
            # Temporary hack to try and repair game pieces for imported fields
            # TODO: Replace this later for proper game piece repairing in the edit dialog
            game_pieces = await GamePiece.all()
            matching_game_pieces = [gp for gp in game_pieces if any(word in name.split() for word in gp.name.split())]
            
            if matching_game_pieces:
                print("WARNING: Game piece not found. Using closest match based on field name: " + matching_game_pieces[0].name)
                game_piece = matching_game_pieces[0]
            else:
                raise HTTPException(status_code=404, detail="Game piece not found")
    else:
        game_piece = None

    if organization_uuid != "":
        organization = await Organization.get_or_none(uuid=organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    if parent_uuid != "":
        parent = await MatchScoutingField.get_or_none(uuid=parent_uuid)
        if not parent:
            raise HTTPException(status_code=404, detail="Section not found")
    else:
        parent = None

    field = await MatchScoutingField.create(
        parent=parent,
        season=season, 
        name=name, 
        field_type=field_type, 
        stat_type=stat_type, 
        game_piece=game_piece, 
        required=required, 
        options=options, 
        order=order, 
        organization=organization
    )
    return field

@router.post("/fields/season/{season_uuid}/edit/{field_uuid}")
async def edit_season_field(
        season_uuid: str, 
        field_uuid: str, 

        parent_uuid: str = Form(...),
        name: str = Form(...), 
        field_type: str = Form(...), 
        stat_type: str = Form(...), 
        game_piece_uuid: str = Form(...), 
        required: bool = Form(...), 
        options: list = Form(...), 
        order: int = Form(...), 
        organization_uuid: str = Form(...), 
        current_user: User = Depends(get_current_user)
    ):

    field = await MatchScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
        
    season = await Season.get_or_none(uuid=season_uuid)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")

    if stat_type == "auton_score" or stat_type == "auton_miss" or stat_type == "teleop_score" or stat_type == "teleop_miss":
        game_piece = await GamePiece.get_or_none(uuid=game_piece_uuid)
        if not game_piece:
            raise HTTPException(status_code=404, detail="Game piece not found")
    else:
        game_piece = None

    if organization_uuid != "":
        organization = await Organization.get_or_none(uuid=organization_uuid)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
    else:
        organization = None

    field.name = name
    field.field_type = field_type
    field.stat_type = stat_type
    field.game_piece = game_piece
    field.required = required
    field.options = options
    field.order = order
    field.organization = organization
    await field.save()
    return field

@router.get("/fields/get_presets")
async def get_match_scouting_field_presets():    
    print(os.getcwd())
    path = Path("./app/match_scouting_presets")
    presets = []

    for file in path.iterdir():
        with open(file, "r") as f:
            presets.append({ "name": file.stem, "preset": json.load(f) })

    return presets

@router.delete("/fields/delete/{field_uuid}")
async def delete_field(field_uuid: str, current_user: User = Depends(get_current_user)):
    field = await MatchScoutingField.get_or_none(uuid=field_uuid)
    if not field:
        raise HTTPException(status_code=404, detail="Field not found")
    await field.delete()
    return {"message": "Field deleted"}