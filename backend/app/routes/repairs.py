from datetime import datetime

from fastapi import APIRouter, Depends


from ..dependencies import Identity, require_superuser
from ..schemas.repairs import EventRepair, GamePieceRepair, MatchScoutingAnswerRepair, MatchScoutingFieldRepair, MatchScoutingSubmissionRepair, PitScoutingAnswerRepair, PitScoutingFieldRepair, RepairResponse, TeamPitRepair
from ..models import Event, GamePiece, MatchScoutingAnswer, MatchScoutingField, MatchScoutingSubmission, PitScoutingAnswer, PitScoutingField, TeamPit
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