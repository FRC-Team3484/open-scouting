from datetime import datetime
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import Identity, require_superuser
from ..schemas.generic import MessageResponse
from ..schemas.repairs import EventRepair, GamePieceRepair, MatchScoutingAnswerRepair, MatchScoutingFieldRepair, MatchScoutingFieldRepairResponse, MatchScoutingSubmissionRepair, PitScoutingAnswerRepair, PitScoutingFieldRepair, PitScoutingFieldRepairResponse, RepairRequest, RepairResponse, TeamPitRepair
from ..models import Event, GamePiece, MatchScoutingAnswer, MatchScoutingField, MatchScoutingSubmission, PitScoutingAnswer, PitScoutingField, Season, TeamPit
from ..utils import IS_DEV


router: APIRouter = APIRouter(
    tags=["Repairs"],
    include_in_schema=IS_DEV
)

async def get_repairable_events() -> list[EventRepair]:
    """
    Get all repairable events

    This supports the following repairs:
        - `Event` is missing a `season`
    """
    events = await Event.filter(season=None).all()

    repairs: list[EventRepair] = []

    for event in events:
        repairs.append(
            EventRepair(
                name=f"Event {event.name} is missing a season",
                data_uuid=event.uuid,
                data_created_at=event.created_at,
                data_type="event",
                repair_type="missing_season"
            )
        )

    return repairs

async def get_repairable_game_pieces() -> list[GamePieceRepair]:
    """
    Get all repairable game pieces

    This supports the following repairs:
        - `GamePiece` is mising a `season`
    """
    game_pieces = await GamePiece.filter(season=None).all()

    repairs: list[GamePieceRepair] = []

    for game_piece in game_pieces:
        repairs.append(
            GamePieceRepair(
                name=f"Game piece {game_piece.name} is missing a season",
                data_uuid=game_piece.uuid,
                data_created_at=game_piece.created_at,
                data_type="game_piece",
                repair_type="missing_season"
            )
        )

    return repairs

async def get_repairable_match_scouting_fields() -> list[MatchScoutingFieldRepair]:
    """
    Get all repairable match scouting fields

    This supports the following repairs:
        - `MatchScoutingField` is missing a `season`
        - `MatchScoutingField` is missing a `game_piece` if `stat_type` is `auton_score`, `auton_miss`, `teleop_score` or `teleop_miss`
    """
    fields_without_season = await MatchScoutingField.filter(season=None).all()
    fields_without_game_piece = await MatchScoutingField.filter(game_piece=None).filter(stat_type__in=["auton_score", "auton_miss", "teleop_score", "teleop_miss"]).all()

    repairs: list[MatchScoutingFieldRepair] = []

    for field in fields_without_season:
        repairs.append(
            MatchScoutingFieldRepair(
                name=f"Match scouting field {field.name} is missing a season",
                data_uuid=field.uuid,
                data_created_at=field.created_at,
                data_type="match_scouting_field",
                repair_type="missing_season"
            )
        )

    for field in fields_without_game_piece:
        repairs.append(
            MatchScoutingFieldRepair(
                name=f"Match scouting field {field.name} is missing a game piece",
                data_uuid=field.uuid,
                data_created_at=field.created_at,
                data_type="match_scouting_field",
                repair_type="missing_game_piece"
            )
        )

    return repairs

async def get_repairable_match_scouting_submissions() -> list[MatchScoutingSubmissionRepair]:
    """
    Get all repairable match scouting submissions

    This supports the following repairs:
        - `MatchScoutingSubmission` is missing an `event`
    """
    submissions = await MatchScoutingSubmission.filter(event=None).all()

    repairs: list[MatchScoutingSubmissionRepair] = []

    for submission in submissions:
        repairs.append(
            MatchScoutingSubmissionRepair(
                name=f"Match scouting submission for team {submission.team_number} in {submission.match_type} match {submission.match_number} is missing an event",
                data_uuid=submission.uuid,
                data_created_at=submission.created_at,
                data_type="match_scouting_submission",
                repair_type="missing_event"
            )
        )

    return repairs

async def get_repairable_match_scouting_answers() -> list[MatchScoutingAnswerRepair]:
    """
    Get all repairable match scouting answers

    This supports the following repairs:
        - `MatchScoutingAnswer` is missing a `field`
        - `MatchScoutingAnswer` is missing a `submission`
    """
    answers_without_field = await MatchScoutingAnswer.filter(field=None).prefetch_related("submission").all()
    answers_without_submission = await MatchScoutingAnswer.filter(submission=None).prefetch_related("field", "field__season").all()

    repairs: list[MatchScoutingAnswerRepair] = []

    for answer in answers_without_field:
        repairs.append(
            MatchScoutingAnswerRepair(
                name=f"Match scouting answer with value {answer.value} and submission {getattr(answer.submission, "uuid", None)} (team {getattr(answer.submission, 'team_number', None)} match {getattr(answer.submission, 'match_number', None)}) is missing a field",
                data_uuid=answer.uuid,
                data_created_at=answer.created_at,
                data_type="match_scouting_answer",
                repair_type="missing_field"
            )
        )

    for answer in answers_without_submission:
        repairs.append(
            MatchScoutingAnswerRepair(
                name=f"Match scouting answer with value {answer.value} and field {getattr(answer.field, 'name', None)} for season {getattr(getattr(answer.field, 'season', None), 'year', None)} is missing a submission",
                data_uuid=answer.uuid,
                data_created_at=answer.created_at,
                data_type="match_scouting_answer",
                repair_type="missing_submission"
            )
        )

    return repairs

async def get_repairable_pit_scouting_fields() -> list[PitScoutingFieldRepair]:
    """
    Get all repairable pit scouting fields

    This supports the following repairs:
        - `PitScoutingField` is missing a `season`
    """
    fields_without_season = await PitScoutingField.filter(season=None).all()

    repairs: list[PitScoutingFieldRepair] = []

    for field in fields_without_season:
        repairs.append(
            PitScoutingFieldRepair(
                name=f"Pit scouting field {field.name} is missing a season",
                data_uuid=field.uuid,
                data_created_at=field.created_at,
                data_type="pit_scouting_field",
                repair_type="missing_season"
            )
        )

    return repairs

async def get_repairable_team_pits() -> list[TeamPitRepair]:
    """
    Get all repairable team pits

    This supports the following repairs:
        - `TeamPit` is missing a `season`
        - `TeamPit` is missing an `event`
    """
    pits_without_season = await TeamPit.filter(season=None).prefetch_related("event").all()
    pits_without_event = await TeamPit.filter(event=None).prefetch_related("season").all()

    repairs: list[TeamPitRepair] = []

    for pit in pits_without_season:
        repairs.append(
            TeamPitRepair(
                name=f"Team pit {pit.team_number} at event {getattr(pit.event, 'name', None)} is missing a season",
                data_uuid=pit.uuid,
                data_created_at=pit.created_at,
                data_type="team_pit",
                repair_type="missing_season"
            )
        )

    for pit in pits_without_event:
        repairs.append(
            TeamPitRepair(
                name=f"Team pit {pit.team_number} for season {getattr(pit.season, 'year', None)} is missing an event",
                data_uuid=pit.uuid,
                data_created_at=pit.created_at,
                data_type="team_pit",
                repair_type="missing_event"
            )
        )

    return repairs

async def get_repairable_pit_scouting_answers() -> list[PitScoutingAnswerRepair]:
    """
    Get all repairable pit scouting answers

    This supports the following repairs:
        - `PitScoutingAnswer` is missing a `field`
        - `PitScoutingAnswer` is missing a `team`
    """
    answers_without_field = await PitScoutingAnswer.filter(field=None).prefetch_related("team").all()
    answers_without_team = await PitScoutingAnswer.filter(team=None).prefetch_related("field", "field__season").all()

    repairs: list[PitScoutingAnswerRepair] = []

    for answer in answers_without_field:
        repairs.append(
            PitScoutingAnswerRepair(
                name=f"Pit scouting answer with value {answer.value} and team {getattr(answer.team, 'team_number', None)} is missing a field",
                data_uuid=answer.uuid,
                data_created_at=answer.created_at,
                data_type="pit_scouting_answer",
                repair_type="missing_field"
            )
        )

    for answer in answers_without_team:
        repairs.append(
            PitScoutingAnswerRepair(
                name=f"Pit scouting answer with value {answer.value} and field {getattr(answer.field, 'name', None)} for season {getattr(getattr(answer.field, 'season', None), 'year', None)} is missing a team",
                data_uuid=answer.uuid,
                data_created_at=answer.created_at,
                data_type="pit_scouting_answer",
                repair_type="missing_team"
            )
        )

    return repairs

@router.get("/repairs/get", response_model=list[RepairResponse])
async def get_repairs(identity: Identity = Depends(require_superuser)):
    """
    Get all available repairs

    Requires superuser access

    The following repairs are able to be returned here:
        - `Event` is missing a `season`
        - `GamePiece` is mising a `season`
        - `MatchScoutingField` is missing a `season`
        - `MatchScoutingField` is missing a `game_piece` if `stat_type` is `auton_score`, `auton_miss`, `teleop_score` or `teleop_miss`
        - `MatchScoutingSubmission` is missing an `event`
        - `MatchScoutingAnswer` is missing a `field`
        - `MatchScoutingAnswer` is missing a `submission`
        - `PitScoutingField` is missing a `season`
        - `TeamPit` is missing a `season`
        - `TeamPit` is missing an `event`
        - `PitScoutingAnswer` is missing a `field`
        - `PitScoutingAnswer` is missing a `team`
    """
    
    functions = [
        get_repairable_events,
        get_repairable_game_pieces,
        get_repairable_match_scouting_fields,
        get_repairable_match_scouting_submissions,
        get_repairable_match_scouting_answers,
        get_repairable_pit_scouting_fields,
        get_repairable_team_pits,
        get_repairable_pit_scouting_answers
    ]

    return [
        repair
        for function in functions
        for repair in await function()
    ]

@router.get("/repairs/get/count", response_model=int)
async def get_repair_count(identity: Identity = Depends(require_superuser)):
    """
    Get the number of available repairs

    Requires superuser access

    Returns:
        int: The number of available repairs
    """
    repairs: list[int] = [
        await Event.filter(season=None).count(),
        await GamePiece.filter(season=None).count(),
        await MatchScoutingField.filter(season=None).count(),
        await MatchScoutingField.filter(game_piece=None).filter(stat_type__in=["auton_score", "auton_miss", "teleop_score", "teleop_miss"]).count(),
        await MatchScoutingSubmission.filter(event=None).count(),
        await MatchScoutingAnswer.filter(field=None).count(),
        await MatchScoutingAnswer.filter(submission=None).count(),
        await PitScoutingField.filter(season=None).count(),
        await TeamPit.filter(season=None).count(),
        await TeamPit.filter(event=None).count(),
        await PitScoutingAnswer.filter(field=None).count(),
        await PitScoutingAnswer.filter(team=None).count()
    ]

    return sum(repairs)

# TODO: Remove
@router.post("/repairs/create")
async def create_repairs_for_testing(identity: Identity = Depends(require_superuser)):
    event = await Event.create(season=None, event_code="test_event_code", name="test_event_name", type="test_event_type", city="test_event_city", country="test_event_country", start_date=datetime.now(), end_date=datetime.now(), custom=False)

    piece = await GamePiece.create(season=None, name="test_game_piece_name")

    await MatchScoutingField.create(season=None, name="test_match_scouting_field_name", field_type="section", stat_type="section", game_piece=piece)
    field = await MatchScoutingField.create(season=None, name="test_match_scouting_field_name", field_type="section", stat_type="section", game_piece=None)

    submission = await MatchScoutingSubmission.create(event=None)

    await MatchScoutingAnswer.create(field=field, submission=None)
    await MatchScoutingAnswer.create(field=None, submission=submission)

    pit_field = await PitScoutingField.create(season=None, name="test_pit_scouting_field_name", field_type="text")

    team = await TeamPit.create(season=None, event=event, team_number=1, nickname="test_team_name")
    await TeamPit.create(season=None, event=None, team_number=1, nickname="test_team_name")

    await PitScoutingAnswer.create(field=None, team=team)
    await PitScoutingAnswer.create(field=pit_field, team=None)

    return "Repairs created"

# Get data that can be used for repairs
@router.get("/repairs/get/match_scouting_fields", response_model=list[MatchScoutingFieldRepairResponse])
async def get_all_match_scouting_fields(identity: Identity = Depends(require_superuser)):
    """
    Get all match scouting fields. Used on the admin repair page when setting the match scouting field on a piece of data.

    Requires superuser access

    Returns:
        list[MatchScoutingFieldRepairResponse]: A list of all match scouting fields
    """
    fields = await MatchScoutingField.all().prefetch_related("season", "game_piece")

    return [
        MatchScoutingFieldRepairResponse(
            uuid=field.uuid,
            name=field.name,
            season_year=getattr(field.season, "year", None),
            game_piece_name=getattr(field.game_piece, "name", None),
            archived=field.archived,
            created_at=field.created_at
        )
        for field in fields
    ]

@router.get("/repairs/get/pit_scouting_fields", response_model=list[PitScoutingFieldRepairResponse])
async def get_all_pit_scouting_fields(identity: Identity = Depends(require_superuser)):
    """
    Get all pit scouting fields. Used on the admin repair page when setting the pit scouting field on a piece of data.

    Requires superuser access

    Returns:
        list[PitScoutingFieldRepairResponse]: A list of all pit scouting fields
    """
    fields = await PitScoutingField.all().prefetch_related("season")

    return [
        PitScoutingFieldRepairResponse(
            uuid=field.uuid,
            name=field.name,
            season_year=getattr(field.season, "year", None),
            archived=field.archived,
            created_at=field.created_at
        )
        for field in fields
    ]

# Fix repairs
async def repair_event(data_uuid: UUID, content_uuid: UUID, data_type: Literal["event"], repair_type: Literal["missing_season"]):
    """
    Repair an event

    Parameters:
        data_uuid (`UUID`): The uuid of the event to repair
        content_uuid (`UUID`): The uuid of the season to repair the event with
        data_type (`Literal["event"]`): The type of data to repair
        repair_type (`Literal["missing_season"]`): The type of repair to perform
    """
    event = await Event.get_or_none(uuid=data_uuid)
    season = await Season.get_or_none(uuid=content_uuid)
    
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")
        
    event.season = season

    await event.save()

async def repair_game_piece(data_uuid: UUID, content_uuid: UUID, data_type: Literal["game_piece"], repair_type: Literal["missing_season"]):
    """
    Repair a game piece

    Parameters:
        data_uuid (`UUID`): The uuid of the game piece to repair
        content_uuid (`UUID`): The uuid of the season to repair the game piece with
        data_type (`Literal["game_piece"]`): The type of data to repair
        repair_type (`Literal["missing_season"]`): The type of repair to perform
    """
    game_piece = await GamePiece.get_or_none(uuid=data_uuid)
    season = await Season.get_or_none(uuid=content_uuid)
    
    if game_piece is None:
        raise HTTPException(status_code=404, detail="Game piece not found")
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")
        
    game_piece.season = season

    await game_piece.save()

async def repair_match_scouting_field(data_uuid: UUID, content_uuid: UUID, data_type: Literal["match_scouting_field"], repair_type: Literal["missing_season", "missing_game_piece"]):
    """
    Repair a match scouting field

    Parameters:
        data_uuid (`UUID`): The uuid of the match scouting field to repair
        content_uuid (`UUID`): The uuid of the season or game piece to repair the match scouting field with
        data_type (`Literal["match_scouting_field"]`): The type of data to repair
        repair_type (`Literal["missing_season", "missing_game_piece"]`): The type of repair to perform
    """
    match_scouting_field = await MatchScoutingField.get_or_none(uuid=data_uuid)

    if match_scouting_field is None:
        raise HTTPException(status_code=404, detail="Match scouting field not found")

    if repair_type == "missing_season":
        season = await Season.get_or_none(uuid=content_uuid)
        if season is None:
            raise HTTPException(status_code=404, detail="Season not found")
        match_scouting_field.season = season
    elif repair_type == "missing_game_piece":
        game_piece = await GamePiece.get_or_none(uuid=content_uuid)
        if game_piece is None:
            raise HTTPException(status_code=404, detail="Game piece not found")
        match_scouting_field.game_piece = game_piece

    await match_scouting_field.save()

async def repair_match_scouting_submission(data_uuid: UUID, event_code: str, data_type: Literal["match_scouting_submission"], repair_type: Literal["missing_event"]):
    """
    Repair a match scouting submission

    Parameters:
        data_uuid (`UUID`): The uuid of the match scouting submission to repair
        event_code (`str`): The event code of the event to repair the match scouting submission with
        data_type (`Literal["match_scouting_submission"]`): The type of data to repair
        repair_type (`Literal["missing_event"]`): The type of repair to perform
    """
    match_scouting_submission = await MatchScoutingSubmission.get_or_none(uuid=data_uuid)
    event = await Event.get_or_none(event_code=event_code)

    if match_scouting_submission is None:
        raise HTTPException(status_code=404, detail="Match scouting submission not found")
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    match_scouting_submission.event = event

    await match_scouting_submission.save()

async def repair_match_scouting_answer(data_uuid: UUID, content_uuid: UUID, data_type: Literal["match_scouting_answer"], repair_type: Literal["missing_field", "missing_submission"]):
    """
    Repair a match scouting answer

    Parameters:
        data_uuid (`UUID`): The uuid of the match scouting answer to repair
        content_uuid (`UUID`): The uuid of the field or team to repair the match scouting answer with
        data_type (`Literal["match_scouting_answer"]`): The type of data to repair
        repair_type (`Literal["missing_field", "missing_team"]`): The type of repair to perform
    """
    match_scouting_answer = await MatchScoutingAnswer.get_or_none(uuid=data_uuid)

    if match_scouting_answer is None:
        raise HTTPException(status_code=404, detail="Match scouting answer not found")

    if repair_type == "missing_field":
        match_scouting_field = await MatchScoutingField.get_or_none(uuid=content_uuid)
        if match_scouting_field is None:
            raise HTTPException(status_code=404, detail="Match scouting field not found")
        match_scouting_answer.match_scouting_field = match_scouting_field
    elif repair_type == "missing_submission":
        match_scouting_submission = await MatchScoutingSubmission.get_or_none(uuid=content_uuid)
        if match_scouting_submission is None:
            raise HTTPException(status_code=404, detail="Match scouting submission not found")
        match_scouting_answer.match_scouting_submission = match_scouting_submission

    await match_scouting_answer.save()

async def repair_pit_scouting_field(data_uuid: UUID, content_uuid: UUID, data_type: Literal["pit_scouting_field"], repair_type: Literal["missing_season"]):
    """
    Repair a pit scouting field

    Parameters:
        data_uuid (`UUID`): The uuid of the pit scouting field to repair
        content_uuid (`UUID`): The uuid of the season or game piece to repair the pit scouting field with
        data_type (`Literal["pit_scouting_field"]`): The type of data to repair
        repair_type (`Literal["missing_season"]`): The type of repair to perform
    """
    pit_scouting_field = await PitScoutingField.get_or_none(uuid=data_uuid)
    season = await Season.get_or_none(uuid=content_uuid)

    if pit_scouting_field is None:
        raise HTTPException(status_code=404, detail="Pit scouting field not found")
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")

    pit_scouting_field.season = season

    await pit_scouting_field.save()

async def repair_team_pit(data_uuid: UUID, content_uuid: UUID | None, data_type: Literal["team_pit"], repair_type: Literal["missing_season", "missing_event"], event_code: str | None):
    """
    Repair a team pit

    Parameters:
        data_uuid (`UUID`): The uuid of the team pit to repair
        content_uuid (`UUID`): The uuid of the season or game piece to repair the team pit with
        data_type (`Literal["team_pit"]`): The type of data to repair
        repair_type (`Literal["missing_season", "missing_event"]`): The type of repair to perform
    """
    team_pit = await TeamPit.get_or_none(uuid=data_uuid)

    if team_pit is None:
        raise HTTPException(status_code=404, detail="Team pit not found")

    if repair_type == "missing_season":
        season = await Season.get_or_none(uuid=content_uuid)
        if season is None:
            raise HTTPException(status_code=404, detail="Season not found")
        team_pit.season = season
    elif repair_type == "missing_event":
        # TODO: Handle if event has not yet been created on the server
        event = await Event.get_or_none(event_code=event_code)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        team_pit.event = event

    await team_pit.save()

async def repair_pit_scouting_answer(data_uuid: UUID, content_uuid: UUID, data_type: Literal["pit_scouting_answer"], repair_type: Literal["missing_field", "missing_team"]):
    """
    Repair a pit scouting answer

    Parameters:
        data_uuid (`UUID`): The uuid of the pit scouting answer to repair
        content_uuid (`UUID`): The uuid of the field or team to repair the pit scouting answer with
        data_type (`Literal["pit_scouting_answer"]`): The type of data to repair
        repair_type (`Literal["missing_field", "missing_team"]`): The type of repair to perform
    """
    pit_scouting_answer = await PitScoutingAnswer.get_or_none(uuid=data_uuid)

    if pit_scouting_answer is None:
        raise HTTPException(status_code=404, detail="Pit scouting answer not found")

    if repair_type == "missing_field":
        pit_scouting_field = await PitScoutingField.get_or_none(uuid=content_uuid)
        if pit_scouting_field is None:
            raise HTTPException(status_code=404, detail="Pit scouting field not found")
        pit_scouting_answer.pit_scouting_field = pit_scouting_field
    elif repair_type == "missing_team":
        team = await TeamPit.get_or_none(uuid=content_uuid)
        if team is None:
            raise HTTPException(status_code=404, detail="Team not found")
        pit_scouting_answer.team = team

    await pit_scouting_answer.save()

@router.post(f"/repairs/fix", response_model=MessageResponse)
async def fix_repair(data: RepairRequest, identity: Identity = Depends(require_superuser)):
    """
    Fix a repair

    Requires superuser access

    Parameters:
        data (`RepairRequest`): The data to fix

    Returns:
        `MessageResponse`: A message indicating that the repair was fixed (or failed to fix)
    """
    if data.data_type == "event":
        await repair_event(data.data_uuid, data.content_uuid, data.data_type, data.repair_type)
    elif data.data_type == "game_piece":
        await repair_game_piece(data.data_uuid, data.content_uuid, data.data_type, data.repair_type)
    elif data.data_type == "match_scouting_field":
        await repair_match_scouting_field(data.data_uuid, data.content_uuid, data.data_type, data.repair_type)
    elif data.data_type == "match_scouting_submission":
        await repair_match_scouting_submission(data.data_uuid, data.event_code, data.data_type, data.repair_type)
    elif data.data_type == "match_scouting_answer":
        await repair_match_scouting_answer(data.data_uuid, data.content_uuid, data.data_type, data.repair_type)
    elif data.data_type == "pit_scouting_field":
        await repair_pit_scouting_field(data.data_uuid, data.content_uuid, data.data_type, data.repair_type)
    elif data.data_type == "team_pit":
        await repair_team_pit(data.data_uuid, data.content_uuid, data.data_type, data.repair_type, data.event_code)
    elif data.data_type == "pit_scouting_answer":
        await repair_pit_scouting_answer(data.data_uuid, data.content_uuid, data.data_type, data.repair_type)

    return MessageResponse(message="Repair fixed")