from django.utils.translation import gettext_lazy as _
from django.utils.functional import Promise
from django.utils.encoding import force_str
import copy


def force_str_in_dict(obj):
    """Recursively convert lazy translation objects to regular strings in dicts/lists."""
    if isinstance(obj, Promise):
        return force_str(obj)
    elif isinstance(obj, dict):
        return {key: force_str_in_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [force_str_in_dict(item) for item in obj]
    elif isinstance(obj, (list, tuple)):
        return [force_str_in_dict(item) for item in obj]
    else:
        return obj


def get_season_fields(year):
    season_mapping = {"2024": crescendo, "2025": reefscape, "2026": rebuilt}

    # Deep copy to avoid modifying original
    season_fields = copy.deepcopy(season_mapping.get(year, []))

    # Add `main` at the beginning
    if isinstance(main, list):
        season_fields = copy.deepcopy(main) + season_fields
    else:
        season_fields.insert(0, copy.deepcopy(main))

    # Assign a universal order across all fields
    order_index = 0
    for section in season_fields:
        if isinstance(section, dict) and "fields" in section:
            for field in section["fields"]:
                if isinstance(field, dict):
                    field.setdefault("order", order_index)
                    order_index += 1

    # Convert lazy translation proxies to real strings
    return force_str_in_dict(season_fields)


# ----------
# Main Fields
# ----------
main = [
    {
        "section": _("Main"),
        "simple_name": "main",
        "fields": [
            {
                "name": _("Team Number"),
                "simple_name": "team_number",
                "type": "large_integer",
                "required": True,
                "stat_type": "ignore",
                "game_piece": "",
            },
            {
                "name": _("Match Number"),
                "simple_name": "match_number",
                "type": "large_integer",
                "required": True,
                "stat_type": "ignore",
                "game_piece": "",
            },
            {
                "name": _("Match Type"),
                "simple_name": "match_type",
                "type": "choice",
                "choices": [
                    (_("N/A"), "N/A"),
                    (_("Qualification Match"), "qualification_match"),
                    (_("Playoff Match"), "playoff_match"),
                    (_("Practice Match"), "practice_match"),
                    (_("Other Match"), "other_match"),
                ],
                "required": False,
                "stat_type": "ignore",
                "game_piece": "",
            },
        ],
    },
]


# ----------
# 2024
# ----------
crescendo = [
    {
        "section": _("Auton"),
        "simple_name": "auton",
        "fields": [
            {
                "name": _("Speaker Shot"),
                "simple_name": "speaker_shot",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 30,
                "required": False,
                "stat_type": "auton_score",
                "game_piece": "note",
            },
            {
                "name": _("Amp Shot"),
                "simple_name": "amp_shot",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 30,
                "required": False,
                "stat_type": "auton_score",
                "game_piece": "note",
            },
        ],
    },
    {
        "section": _("Teleop"),
        "simple_name": "teleop",
        "fields": [
            {
                "section": _("Speaker"),
                "simple_name": "teleop_speaker",
                "fields": [
                    {
                        "name": _("Speaker Shot"),
                        "simple_name": "speaker_shot",
                        "type": "integer",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 30,
                        "required": False,
                        "stat_type": "score",
                        "game_piece": "note",
                    },
                    {
                        "name": _("Speaker Misses"),
                        "simple_name": "speaker_miss",
                        "type": "integer",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 30,
                        "required": False,
                        "stat_type": "miss",
                        "game_piece": "note",
                    },
                ],
            },
            {
                "section": _("Amp"),
                "simple_name": "teleop_amp",
                "fields": [
                    {
                        "name": _("Amp Shots"),
                        "simple_name": "amp_shot",
                        "type": "integer",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 30,
                        "required": False,
                        "stat_type": "score",
                        "game_piece": "note",
                    },
                    {
                        "name": _("Amp Misses"),
                        "simple_name": "amp_miss",
                        "type": "integer",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 30,
                        "required": False,
                        "stat_type": "miss",
                        "game_piece": "note",
                    },
                ],
            },
        ],
    },
    {
        "section": _("Extra Information"),
        "simple_name": "extra_information",
        "fields": [
            {
                "name": _("Left Starting Zone"),
                "simple_name": "left_starting_zone",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Shoot Distance"),
                "simple_name": "shoot_distance",
                "type": "multiple_choice",
                "choices": [
                    (_("N/A"), "N/A"),
                    (_("Close"), "close"),
                    (_("Mid Field"), "mid_field"),
                    (_("Far"), "far"),
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Floor Pickup"),
                "simple_name": "floor_pickup",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Climb"),
                "simple_name": "climb",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Scored Trap"),
                "simple_name": "scored_trap",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Feeder Station Pickup"),
                "simple_name": "feeder_station_pickup",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Moved During Auto"),
                "simple_name": "moved_during_auto",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
        ],
    },
    {
        "section": _("Additional Notes"),
        "simple_name": "additional_notes",
        "fields": [
            {
                "name": _("Additional Notes or Comments"),
                "simple_name": "notes",
                "type": "text",
                "required": False,
                "stat_type": "other",
                "game_piece": "",
            },
        ],
    },
]

# ----------
# 2025
# ----------
reefscape = [
    {
        "section": _("Auton"),
        "simple_name": "auton",
        "fields": [
            {
                "name": _("Left Starting Zone"),
                "simple_name": "auton_moved",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Coral Scored in Reef"),
                "simple_name": "auton_coral_scored",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "auton_score",
                "game_piece": "coral",
            },
            {
                "name": _("Coral Dropped"),
                "simple_name": "auton_coral_dropped",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "auton_miss",
                "game_piece": "coral",
            },
            {
                "name": _("Algae Removed"),
                "simple_name": "auton_algae_removed",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "auton_score",
                "game_piece": "algae",
            },
            {
                "name": _("Algae Scored in Net"),
                "simple_name": "auton_algae_scored_in_net",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "auton_score",
                "game_piece": "algae",
            },
            {
                "name": _("Algae Scored in Processor"),
                "simple_name": "auton_algae_scored_in_processor",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "auton_score",
                "game_piece": "algae",
            },
            {
                "name": _("Algae Score Failed"),
                "simple_name": "algae_score_failed",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "auton_miss",
                "game_piece": "algae",
            },
        ],
    },
    {
        "section": _("Teleop"),
        "simple_name": "teleop",
        "fields": [
            {
                "name": _("Coral Scored in Reef"),
                "simple_name": "coral_scored",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "score",
                "game_piece": "coral",
            },
            {
                "name": _("Coral Dropped"),
                "simple_name": "coral_dropped",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "miss",
                "game_piece": "coral",
            },
            {
                "name": _("Algae Removed"),
                "simple_name": "algae_removed",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "score",
                "game_piece": "algae",
            },
            {
                "name": _("Algae Scored in Net"),
                "simple_name": "algae_scored_in_net",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "score",
                "game_piece": "algae",
            },
            {
                "name": _("Algae Scored in Processor"),
                "simple_name": "algae_scored_in_processor",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "score",
                "game_piece": "algae",
            },
            {
                "name": _("Algae Score Failed"),
                "simple_name": "algae_score_failed",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "stat_type": "miss",
                "game_piece": "algae",
            },
        ],
    },
    {
        "section": _("Extra Information"),
        "simple_name": "extra_information",
        "fields": [
            {
                "name": _("Coral Levels"),
                "simple_name": "coral_levels",
                "type": "multiple_choice",
                "choices": [
                    (_("Level 1"), "level_1"),
                    (_("Level 2"), "level_2"),
                    (_("Level 3"), "level_3"),
                    (_("Level 4"), "level_4"),
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Feeder Station Pickup"),
                "simple_name": "feeder_pickup",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("End Location"),
                "simple_name": "end_location",
                "type": "choice",
                "choices": [
                    (_("N/A"), "N/A"),
                    (_("Barge Zone"), "barge_zone"),
                    (_("Shallow Cage"), "shallow_cage"),
                    (_("Deep Cage"), "deep_cage"),
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Driver Skill"),
                "simple_name": "driver_skill",
                "type": "choice",
                "choices": [
                    (_("N/A"), "N/A"),
                    (_("1 - Poor"), "1_poor"),
                    (_("2 - Okay"), "2_okay"),
                    (_("3 - Decent"), "3_decent"),
                    (_("4 - Good"), "4_good"),
                    (_("5 - Great"), "5_great"),
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Defense"),
                "simple_name": "defense",
                "type": "choice",
                "choices": [
                    (_("N/A"), "N/A"),
                    (_("1 - Poor"), "1_poor"),
                    (_("2 - Okay"), "2_okay"),
                    (_("3 - Decent"), "3_decent"),
                    (_("4 - Good"), "4_good"),
                    (_("5 - Great"), "5_great"),
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Penalities"),
                "simple_name": "penalities",
                "type": "choice",
                "choices": [
                    (_("N/A"), "N/A"),
                    (_("Minor Foul"), "minor_foul"),
                    (_("Major Foul"), "major_foul"),
                    (_("Yellow Card"), "yellow_card"),
                    (_("Red Card"), "red_card"),
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Robot was damaged and/or disabled during the match"),
                "simple_name": "disabled",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
        ],
    },
    {
        "section": _("Additional Notes"),
        "simple_name": "additional_notes",
        "fields": [
            {
                "name": _("Additional Notes or Comments"),
                "simple_name": "notes",
                "type": "text",
                "required": False,
                "stat_type": "other",
                "game_piece": "",
            },
        ],
    },
]

# ----------
# 2026
# ----------
rebuilt = [
    {
        "section": _("Auton"),
        "simple_name": "auton",
        "fields": [
            {
                "name": _("Left Starting Zone"),
                "simple_name": "auton_moved",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Fuel Scored in Hub"),
                "simple_name": "auton_fuel_scored",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 100,
                "required": False,
                "stat_type": "auton_score",
                "game_piece": "fuel",
            },
            {
                "name": _("Climbed Level 1"),
                "simple_name": "auton_climbed",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Gathered Additional Pieces in Auton"),
                "simple_name": "auton_gathered_pieces",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
        ],
    },
    {
        "section": _("Teleop"),
        "simple_name": "teleop",
        "fields": [
            {
                "name": _("Fuel Scored in Hub"),
                "simple_name": "fuel_scored",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 500,
                "required": False,
                "stat_type": "score",
                "game_piece": "fuel",
            },
            {
                "name": _("Climbed"),
                "simple_name": "climbed",
                "type": "multiple_choice",
                "choices": [
                    (_("N/A"), "na"),
                    (_("Level 1"), "level_1"),
                    (_("Level 2"), "level_2"),
                    (_("Level 3"), "level_3"),
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
        ],
    },
    {
        "section": _("Extra Information"),
        "simple_name": "extra_information",
        "fields": [
            {
                "name": _("Ground Pickup"),
                "simple_name": "ground_pickup",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Outpost Pickup"),
                "simple_name": "outpost_pickup",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
        ],
    },
    {
        "section": _("Additional Notes"),
        "simple_name": "additional_notes",
        "fields": [
            {
                "name": _("Robot was damaged and/or disabled during the match"),
                "simple_name": "disabled",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": _("Additional Notes or Comments"),
                "simple_name": "notes",
                "type": "text",
                "required": False,
                "stat_type": "other",
                "game_piece": "",
            },
        ],
    },
]