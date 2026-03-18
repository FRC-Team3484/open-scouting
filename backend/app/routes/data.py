from collections import defaultdict
import json
from statistics import mean
from typing import Annotated

from fastapi import APIRouter, Query

from ..utils import IS_DEV
from ..models import MatchScoutingAnswer, MatchScoutingField, MatchScoutingSubmission, Season, TeamPit
from ..utils import get_season


router: APIRouter = APIRouter(
    tags=["Data"],
    include_in_schema=IS_DEV
)

# TODO: This needs a proper response_model
@router.get("/data/filters")
async def get_data_filters(
        year: int,
        event_codes: Annotated[str | None, Query()] = None,
        team_numbers: Annotated[str | None, Query()] = None
    ):
    """
    For a year, list of event codes, and list of team numbers, return a JSON object 
        containing the available filters that can additionally be applied

    For example, if just a year is given, return all team numbers and events with data on the server.
    If a year and event code is given, return all team numbers for that event and year with data on the server.
    If a year and multiple event codes are given, return all team numbers which have data on the server for those event codes and year.
    If a year and a team number is given, return all event codes which have data on the server for that team number and year.
    If a year and multiple team numbers are given, return all event codes which have data on the server for those team numbers and year.
    """
    season: Season = await get_season(year=year)

    if event_codes:
        event_codes = [
            int(n) for n in event_codes.split(",")
            if n.strip().isdigit()
        ]

    if team_numbers:
        team_numbers = [
            int(n) for n in team_numbers.split(",")
            if n.strip().isdigit()
        ]

    qs = MatchScoutingSubmission.filter(
        event__season=season
    ).select_related("event")

    if event_codes:
        qs = qs.filter(event__event_code__in=event_codes)

    if team_numbers:
        qs = qs.filter(team_number__in=team_numbers)

    events = await qs.distinct().values(
        event_code="event__event_code",
        event_name="event__name",
    )

    # TEAMS
    teams = await qs.distinct().values(
        team_number="team_number"
    )

    return {
        "events": events,
        "teams": teams,
    }

# TODO: This needs a proper response_model
@router.get("/data/get")
async def get_data(
        year: int,
        event_codes: Annotated[str | None, Query()] = None,
        team_numbers: Annotated[str | None, Query()] = None
    ):
    """
    Given a year, event codes, and team numbers, return the data that matches those filters

    Data should be structured based on the stat_type and game_piece of the associated MatchScoutingField.
    The data should be a list of JSON objects. Each object represents a team with data. In that object,
        there should be four lists: teleop, auton, capability, other
    teleop and auton should be a list of JSON objects, for each game_piece for that season.
        Then, for each game piece, it should be a list of JSON objects that represents each individual field with type: auton_score, auton_miss, teleop_score, teleop_miss
        These fields should have the field type, name, uuid, list of all data points, and the minimum, the maximum, and the average (if applicable).
    
    For example, there are two game pieces. Coral and Algae. There is a field for how much coral was scored and how much were dropped, both as a teleop_score.
        There will be a list of JSON objects for each team. In the team object, inside the teleop list, there should be two additional lists, one for coral and one for algae.
        Then there will two more JSON objects for both of those fields, with the field type, name, uuid, and list of all data points.

    Next, for capabilities, find each field that is a capability and find the percentages of each value occurrence. This will most likely 
        be something that is a multiple_choice or choice MatchScoutingField, and we'll want to show how often each value occurred using something like a pie chart.

    Finally, for other, simply return the same field information and the value, as this will likely be a text input.

    [
        {
            "team_number": 1234,
            "nickname": "Team 1234",
            "teleop": [
                "coral": [
                    {
                        "field_uuid": "uuid",
                        "field_type": "small_number",
                        "field_name": "Coral scored",
                        "values": [1, 2, 3, ...],
                        "min": 0,
                        "max": 100,
                        "avg": 50
                    },
                    {
                        "field_uuid": "uuid",
                        "field_type": "small_number",
                        "field_name": "Coral dropped",
                        "values": [1, 2, 3, ...],
                        "min": 0,
                        "max": 100,
                        "avg": 50
                    }
                ],
                "algae": [...],
            ],
            "auton": [...],
            "capability": [
                {
                    "field_uuid": "uuid",
                    "field_type": "choice",
                    "field_name": "Climb level",
                    "values": ["low", "medium", "high"],
                    "percentages": [
                        {
                            "value": "low",
                            "percentage": 50
                        }, {
                            "value": "medium",
                            "percentage": 25
                        }, {
                            "value": "high",
                            "percentage": 25
                        }
                    ],
                    ...
                }
            ],
            "other": [
                {
                    "field_uuid": "uuid",
                    "field_type": "string",
                    "field_name": "Notes",
                    "value": "Some notes",
                },
                ...
            ]
        },
        ...
    ]
    """
    season: Season = await get_season(year=year)

    if event_codes:
        event_codes = [
            n.strip() for n in event_codes.split(",")
            if n.strip().isalpha()
        ]

    if team_numbers:
        team_numbers = [
            int(n) for n in team_numbers.split(",")
            if n.strip().isdigit()
        ]

    submissions_qs = MatchScoutingSubmission.filter(
        event__season=season
    ).select_related("event")

    if event_codes:
        submissions_qs = submissions_qs.filter(event__event_code__in=event_codes)

    if team_numbers:
        submissions_qs = submissions_qs.filter(team_number__in=team_numbers)

    submissions = await submissions_qs

    if not submissions:
        return []

    submission_ids = [s.uuid for s in submissions]

    answers = await MatchScoutingAnswer.filter(
        submission_id__in=submission_ids,
        field__stat_type__not="ignore",
    ).select_related(
        "field",
        "field__game_piece",
        "submission",
    )

    # Load team nicknames from TeamPit (best available source)
    team_pits = await TeamPit.filter(
        season=season,
        team_number__in={s.team_number for s in submissions}
    )

    team_names = {
        tp.team_number: tp.nickname for tp in team_pits
    }

    # ------------------------
    # Data structure
    # ------------------------
    teams = defaultdict(lambda: {
        "team_number": None,
        "nickname": None,
        "teleop": defaultdict(list),
        "auton": defaultdict(list),
        "capability": [],
        "other": [],
        "summary": [],
    })

    # Helper: numeric conversion
    def parse_number(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    # ------------------------
    # Aggregate raw values
    # ------------------------
    field_values = defaultdict(list)

    for ans in answers:
        team_number = ans.submission.team_number
        field = ans.field

        teams[team_number]["team_number"] = team_number
        teams[team_number]["nickname"] = team_names.get(team_number)

        key = (team_number, field.uuid)
        field_values[key].append({
            "match_number": ans.submission.match_number,
            "value": json.loads(ans.value),
        })
        field_values[key] = sorted(field_values[key], key=lambda x: x["match_number"])

    # ------------------------
    # Process fields
    # ------------------------
    fields = await MatchScoutingField.filter(
        season=season,
        stat_type__not="ignore"
    ).select_related("game_piece")

    fields_by_uuid = {f.uuid: f for f in fields}

    for (team_number, field_uuid), raw_values in field_values.items():
        field = fields_by_uuid[field_uuid]
        stat_type = field.stat_type

        # NUMERIC (auton / teleop)
        if stat_type in {
            "auton_score", "auton_miss",
            "teleop_score", "teleop_miss"
        }:
            values = [{"match_number": v["match_number"], "value": parse_number(v["value"])} for v in raw_values if v["value"] is not None]

            if not values:
                continue

            game_piece = field.game_piece.name

            bucket = "auton" if stat_type.startswith("auton") else "teleop"
            numeric_values = [parse_number(v["value"]) for v in values if v["value"] is not None]

            if numeric_values:
                teams[team_number][bucket][game_piece].append({
                    "field_uuid": str(field.uuid),
                    "field_type": field.field_type,
                    "field_name": field.name,
                    "values": values,
                    "min": min(numeric_values),
                    "max": max(numeric_values),
                    "avg": mean(numeric_values)
                })

        # CAPABILITY (percentages)
        elif stat_type == "capability":
            counts = defaultdict(int)

            for v in raw_values:
                raw = v["value"]

                # Decode JSON if needed
                try:
                    decoded = json.loads(raw)
                except (TypeError, json.JSONDecodeError):
                    decoded = raw

                # If the answer is a list, count each item
                if isinstance(decoded, list):
                    for item in decoded:
                        counts[item] += 1
                else:
                    counts[decoded] += 1

            total = sum(counts.values())

            teams[team_number]["capability"].append({
                "field_uuid": str(field.uuid),
                "field_type": field.field_type,
                "field_name": field.name,
                "values": list(counts.keys()),
                "percentages": [
                    {
                        "value": val,
                        "percentage": round((count / total) * 100, 2)
                    }
                    for val, count in counts.items()
                ]
            })

        # OTHER (text / misc)
        elif stat_type == "other":
            teams[team_number]["other"].append({
                "field_uuid": str(field.uuid),
                "field_type": field.field_type,
                "field_name": field.name,
                "values": raw_values
            })

    # ------------------------
    # Build summary per team (only numeric and capability fields)
    # ------------------------
    numeric_stat_types = {"auton_score", "auton_miss", "teleop_score", "teleop_miss"}

    for team_number in list(teams.keys()):
        summary_items = []
        # find all field entries for this team
        for (t_num, field_uuid), raw_values in field_values.items():
            if t_num != team_number:
                continue
            field = fields_by_uuid.get(field_uuid)
            if not field:
                continue
            stat_type = field.stat_type

            # Numeric summary entries: include list of values and avg
            if stat_type in numeric_stat_types:
                numeric_values = [parse_number(v["value"]) for v in raw_values if parse_number(v["value"]) is not None]
                if not numeric_values:
                    continue
                summary_items.append({
                    "field_uuid": str(field.uuid),
                    "field_name": field.name,
                    "stat_type": stat_type,
                    "avg": mean(numeric_values),
                    "values": numeric_values
                })

            # Capability summary entries: include dict of value -> percentage
            elif stat_type == "capability":
                counts = defaultdict(int)
                for v in raw_values:
                    raw = v["value"]
                    try:
                        decoded = json.loads(raw)
                    except (TypeError, json.JSONDecodeError):
                        decoded = raw

                    if isinstance(decoded, list):
                        for item in decoded:
                            counts[item] += 1
                    else:
                        counts[decoded] += 1

                total = sum(counts.values())
                if total == 0:
                    continue

                percentages = {val: round((count / total) * 100, 2) for val, count in counts.items()}

                summary_items.append({
                    "field_uuid": str(field.uuid),
                    "field_name": field.name,
                    "stat_type": "capability",
                    "avg": "",
                    "values": percentages
                })

        teams[team_number]["summary"] = summary_items

    # Convert defaultdicts to lists
    result = []
    for team in teams.values():
        team["teleop"] = dict(team["teleop"])
        team["auton"] = dict(team["auton"])
        result.append(team)

    return result