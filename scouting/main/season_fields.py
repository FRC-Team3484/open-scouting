def get_season_fields(year):
    season_mapping = {"2024": crescendo, "2025": reefscape}

    season_fields = season_mapping.get(
        year, []
    ).copy()  # Copy to avoid modifying original lists

    if isinstance(main, list):
        season_fields = main + season_fields  # Ensure `main` is properly included
    else:
        season_fields.insert(0, main)

    # Assign a universal order across all fields
    order_index = 0
    for section in season_fields:
        if isinstance(section, dict) and "fields" in section:
            for field in section["fields"]:
                if isinstance(field, dict):  # Ensure field is a dictionary
                    field.setdefault("order", order_index)
                    order_index += 1  # Increment order globally

    return season_fields


# ----------
# Main Fields
# ----------
main = [
    {
        "section": "Main",
        "simple_name": "main",
        "fields": [
            {
                "name": "Team Number",
                "simple_name": "team_number",
                "type": "large_integer",
                "required": True,
                "stat_type": "ignore",
                "game_piece": "",
            },
            {
                "name": "Match Number",
                "simple_name": "match_number",
                "type": "large_integer",
                "required": True,
                "stat_type": "ignore",
                "game_piece": "",
            },
            {
                "name": "Match Type",
                "simple_name": "match_type",
                "type": "choice",
                "choices": [
                    "N/A",
                    "Qualification Match",
                    "Playoff Match",
                    "Practice Match",
                    "Other Match",
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
        "section": "Auton",
        "simple_name": "auton",
        "fields": [
            {
                "name": "Speaker Shot",
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
                "name": "Amp Shot",
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
        "section": "Teleop",
        "simple_name": "teleop",
        "fields": [
            {
                "section": "Speaker",
                "simple_name": "teleop_speaker",
                "fields": [
                    {
                        "name": "Speaker Shot",
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
                        "name": "Speaker Misses",
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
                "section": "Amp",
                "simple_name": "teleop_amp",
                "fields": [
                    {
                        "name": "Amp Shots",
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
                        "name": "Amp Misses",
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
        "section": "Extra Information",
        "simple_name": "extra_information",
        "fields": [
            {
                "name": "Left Starting Zone",
                "simple_name": "left_starting_zone",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Shoot Distance",
                "simple_name": "shoot_distance",
                "type": "multiple_choice",
                "choices": ["N/A", "Close", "Mid Field", "Far"],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Floor Pickup",
                "simple_name": "floor_pickup",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Climb",
                "simple_name": "climb",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Scored Trap",
                "simple_name": "scored_trap",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Feeder Station Pickup",
                "simple_name": "feeder_station_pickup",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Moved During Auto",
                "simple_name": "moved_during_auto",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
        ],
    },
    {
        "section": "Additional Notes",
        "simple_name": "additional_notes",
        "fields": [
            {
                "name": "Additional Notes or Comments",
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
        "section": "Auton",
        "simple_name": "auton",
        "fields": [
            {
                "name": "Left Starting Zone",
                "simple_name": "auton_moved",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Coral Scored in Reef",
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
                "name": "Coral Dropped",
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
                "name": "Algae Removed",
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
                "name": "Algae Scored in Net",
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
                "name": "Algae Scored in Processor",
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
                "name": "Algae Score Failed",
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
        "section": "Teleop",
        "simple_name": "teleop",
        "fields": [
            {
                "name": "Coral Scored in Reef",
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
                "name": "Coral Dropped",
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
                "name": "Algae Removed",
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
                "name": "Algae Scored in Net",
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
                "name": "Algae Scored in Processor",
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
                "name": "Algae Score Failed",
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
        "section": "Extra Information",
        "simple_name": "extra_information",
        "fields": [
            {
                "name": "Coral Levels",
                "simple_name": "coral_levels",
                "type": "multiple_choice",
                "choices": ["Level 1", "Level 2", "Level 3", "Level 4"],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Feeder Station Pickup",
                "simple_name": "feeder_pickup",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "End Location",
                "simple_name": "end_location",
                "type": "choice",
                "choices": ["N/A", "Barge Zone", "Shallow Cage", "Deep Cage"],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Driver Skill",
                "simple_name": "driver_skill",
                "type": "choice",
                "choices": [
                    "N/A",
                    "1 - Poor",
                    "2 - Okay",
                    "3 - Decent",
                    "4 - Good",
                    "5 - Great",
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Defense",
                "simple_name": "defense",
                "type": "choice",
                "choices": [
                    "N/A",
                    "1 - Poor",
                    "2 - Okay",
                    "3 - Decent",
                    "4 - Good",
                    "5 - Great",
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Penalities",
                "simple_name": "penalities",
                "type": "choice",
                "choices": [
                    "N/A",
                    "Minor Foul",
                    "Major Foul",
                    "Yellow Card",
                    "Red Card",
                ],
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
            {
                "name": "Robot was damaged and/or disabled during the match",
                "simple_name": "disabled",
                "type": "boolean",
                "required": False,
                "stat_type": "capability",
                "game_piece": "",
            },
        ],
    },
    {
        "section": "Additional Notes",
        "simple_name": "additional_notes",
        "fields": [
            {
                "name": "Additional Notes or Comments",
                "simple_name": "notes",
                "type": "text",
                "required": False,
                "stat_type": "other",
                "game_piece": "",
            },
        ],
    },
]
