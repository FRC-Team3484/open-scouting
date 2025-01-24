def collect_field_names(data):
    result = []

    def traverse(item):
        # If it's a dictionary, process it
        if isinstance(item, dict):
            # Collect "simple_name" and "name" if "section" is not a key in the same dictionary
            if "simple_name" in item and "section" not in item:
                entry = {"simple_name": item["simple_name"]}
                if "name" in item:
                    entry["name"] = item["name"]
                if "order" in item:  # Include the order if available
                    entry["order"] = item["order"]
                result.append(entry)
            elif "name" in item and "section" not in item:
                entry = {"name": item["name"]}
                if "order" in item:  # Include the order if available
                    entry["order"] = item["order"]
                result.append(entry)
            # Traverse "fields" if present
            if "fields" in item and isinstance(item["fields"], list):
                for field in item["fields"]:
                    traverse(field)
        # If it's a list, traverse each element
        elif isinstance(item, list):
            for element in item:
                traverse(element)

    traverse(data)
    # Remove duplicates
    unique_results = [dict(entry) for entry in {frozenset(e.items()) for e in result}]
    # Sort by order if it exists, else default to 0
    return sorted(unique_results, key=lambda x: x.get("order", 0))


def create_tabulator_headers(data):
    processed = []
    for item in data:
        new_item = {}
        if "name" in item:
            new_item["title"] = item["name"]  # Rename "name" to "title"
        if "simple_name" in item:
            new_item["field"] = item["simple_name"]  # Rename "simple_name" to "field"

        new_item["formatter"] = "adaptable"
        new_item["hozAlign"] = "center"
        new_item["minWidth"] = 100
        new_item["headerWordWrap"] = True

        processed.append(new_item)
    return processed


# ----------
# 2024
# ----------
crescendo = [
    {
        "section": "Main",
        "simple_name": "main",
        "fields": [
            {
                "name": "Team Number",
                "simple_name": "team_number",
                "type": "large_integer",
                "required": True,
                "order": 1,
            },
            {
                "name": "Match Number",
                "simple_name": "match_number",
                "type": "large_integer",
                "required": True,
                "order": 2,
            },
        ],
    },
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
                "order": 3,
            },
            {
                "name": "Amp Shot",
                "simple_name": "amp_shot",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 30,
                "required": False,
                "order": 4,
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
                        "order": 5,
                    },
                    {
                        "name": "Speaker Misses",
                        "simple_name": "speaker_miss",
                        "type": "integer",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 30,
                        "required": False,
                        "order": 6,
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
                        "order": 7,
                    },
                    {
                        "name": "Amp Misses",
                        "simple_name": "amp_miss",
                        "type": "integer",
                        "default": 0,
                        "minimum": 0,
                        "maximum": 30,
                        "required": False,
                        "order": 8,
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
                "order": 9,
            },
            {
                "name": "Shoot Distance",
                "simple_name": "shoot_distance",
                "type": "multiple_choice",
                "choices": ["N/A", "Close", "Mid Field", "Far"],
                "required": False,
                "order": 10,
            },
            {
                "name": "Floor Pickup",
                "simple_name": "floor_pickup",
                "type": "boolean",
                "required": False,
                "order": 11,
            },
            {
                "name": "Climb",
                "simple_name": "climb",
                "type": "boolean",
                "required": False,
                "order": 12,
            },
            {
                "name": "Scored Trap",
                "simple_name": "scored_trap",
                "type": "boolean",
                "required": False,
                "order": 13,
            },
            {
                "name": "Feeder Station Pickup",
                "simple_name": "feeder_station_pickup",
                "type": "boolean",
                "required": False,
                "order": 14,
            },
            {
                "name": "Moved During Auto",
                "simple_name": "moved_during_auto",
                "type": "boolean",
                "required": False,
                "order": 15,
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
                "order": 16,
            },
        ],
    },
]

# ----------
# 2025
# ----------
reefscape = [
    {
        "section": "Main",
        "simple_name": "main",
        "fields": [
            {
                "name": "Team Number",
                "simple_name": "team_number",
                "type": "large_integer",
                "required": True,
                "order": 1,
            },
            {
                "name": "Match Number",
                "simple_name": "match_number",
                "type": "large_integer",
                "required": True,
                "order": 2,
            },
        ],
    },
    {
        "section": "Auton",
        "simple_name": "auton",
        "fields": [
            {
                "name": "Left Starting Zone",
                "simple_name": "auton_moved",
                "type": "boolean",
                "required": False,
                "order": 3,
            },
            {
                "name": "Coral Scored in Reef",
                "simple_name": "auton_coral_scored",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "order": 4,
            },
            {
                "name": "Coral Dropped",
                "simple_name": "auton_coral_dropped",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "order": 5,
            },
            {
                "name": "Algae Removed",
                "simple_name": "auton_algae_removed",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "order": 6,
            },
            {
                "name": "Algae Scored in Net",
                "simple_name": "auton_algae_scored_in_net",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "order": 7,
            },
            {
                "name": "Algae Scored in Processor",
                "simple_name": "auton_algae_scored_in_processor",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "order": 8,
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
                "order": 9,
            },
            {
                "name": "Coral Dropped",
                "simple_name": "coral_dropped",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "order": 10,
            },
            {
                "name": "Algae Removed",
                "simple_name": "algae_removed",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "order": 11,
            },
            {
                "name": "Algae Scored in Net",
                "simple_name": "algae_scored_in_net",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "order": 12,
            },
            {
                "name": "Algae Scored in Processor",
                "simple_name": "algae_scored_in_processor",
                "type": "integer",
                "default": 0,
                "minimum": 0,
                "maximum": 20,
                "required": False,
                "order": 13,
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
                "choices": ["N/A", "Level 1", "Level 2", "Level 3", "Level 4"],
                "required": False,
                "order": 14,
            },
            {
                "name": "Feeder Station Pickup",
                "simple_name": "feeder_pickup",
                "type": "boolean",
                "required": False,
                "order": 15,
            },
            {
                "name": "End Location",
                "simple_name": "end_location",
                "type": "choice",
                "choices": ["N/A", "Barge Zone", "Shallow Cage", "Deep Cage"],
                "required": False,
                "order": 16,
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
                "order": 17,
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
                "order": 18,
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
                "order": 19,
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
                "order": 20,
            },
        ],
    },
]
