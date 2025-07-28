# Formatting Season Fields
> [!NOTE]
> A terminal app is available in [nfoert/open-scouting-utils](https://github.com/nfoert/open-scouting-utils/season-fields-generator/README.md) to simplify this the creation of new season fields

This page documents how the data in `season_fields.py` should be formatted and set up each year, to aid in quickly setting up the json when a new season begins

`season_fields.py` is used to define all the fields and sections needed for scouts to contribute data to the server when scouting. A single field represents a key value pair which is stored in the database for each needed information about the year

You can view the current `season_fields.py` file [here](https://github.com/FRC-Team3484/open-scouting/blob/main/scouting/main/season_fields.py)

## Types of fields
This section demonstrates what each of the available fields are and their parameters

Every field needs at least seven parameters, `name`, `simple_name`, `type`, `required`, `stat_type` and `game_piece`
- `name` indicates the display name of the field, this is the title over the field that appears in the `/submit` UI
- `simple_name` is the simple name of the field, that will be used as the key in the key value pair when the data is stored in the database
- `type` should be one of the following types listed below. This indicates the type of field that is being created, and what data it will return
- `required` indicates if the field is required to have contents to allow the form to be submitted. Setting this parameter to `True` should be kept to a minimum, to prevent frustration during scouting, and allowing for data to be kept empty if it's not needed
- `stat_type` indicates which type of stat it is when displaying data in the advanced data view
    - Possible values are `score` (A score in teleop), `miss` (A miss/drop in teleop), `auton_score` (A score in auton), `auton_miss` (A miss/drop in auton), `capability` (A capability the robot is able to do, for example, if the robot climbed or not), `other` (Some other kind of stat), `ignore` (Don't show these stats in the data view)
- `game_piece` indicates which game piece is used if `stat_type` is `score`, `miss`, `auton_score` or `auton_miss`
    - If any `game_piece` fields are the same, those stats will be grouped together in the advanced data view page
    - This field can be left blank to indicate that no game piece is used for that field/data, for example if it's a capability instead

### `large_integer`
This field should be used for fields like the team number or match number

![large_integer](./images/formatting_season_fields/large_integer.png)

```json
{
    "name": "Team Number",
    "simple_name": "team_number",
    "type": "large_integer",
    "required": True,
    "stat_type": "ignore",
    "game_piece": "",
},
```

This field has no additional parameters

### `integer`
This field should be used for any smaller integer values, like the number of scores or misses

![integer](./images/formatting_season_fields/integer.png)

```json
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
```

- `default` is the default value that the field will show when the form is first loaded
- `minimum` specifies the minimum value that the field can have. The buttons won't allow the number to reach any lower than this
- `maximum` specifics the maximum value that the field can have. The buttons won't allow the number to reach any higher than this

### `boolean`
This field should be used for any value that should be true or false, like if a robot scored in the end game location or not

![boolean](./images/formatting_season_fields/boolean.png)

```json
{
    "name": "Left Starting Zone",
    "simple_name": "left_starting_zone",
    "type": "boolean",
    "required": False,
    "stat_type": "capability",
    "game_piece": "",
},
```

This field has no additional parameters

### `multiple_choice`
This field allows the user to select multiple choices, for example if scouts wanted to indicate multiple distances from with the robot could score from

![multiple_choice](./images/formatting_season_fields/multiple_choice.png)

```json
{
    "name": "Shoot Distance",
    "simple_name": "shoot_distance",
    "type": "multiple_choice",
    "choices": ["N/A", "Close", "Mid Field", "Far"],
    "required": False,
    "stat_type": "capability",
    "game_piece": "",
},
```

- `choices` indicates the list of choices that the scouts can select from. Scouts can select more than one value fpr this field

### `choice`
This field allows the user to select a single choice from a list, in case scouts wanted to indicate something like if the team got any penalties or scored

![choice](./images/formatting_season_fields/choice.png)

```json
{
    "name": "Speaker Shot",
    "simple_name": "speaker_shot",
    "type": "choice",
    "choices": ["N/A", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
    "required": False,
    "stat_type": "score",
    "game_piece": "note",
},
```

- `choices` indicates the list of choices that the scouts can select from. Scouts can only select one value for this field

## Creating Sections
Sections are used to combine multiple fields into one block in the `/submit` UI. Sections can be nested inside of sections for further organization.

The parameters to create a section are as follows:
- `section` is the display name of the section. It's what appears in the title at the top of the section
- `simple_name` is the simple name of the section, it's used internally to render sections in the `/submit` UI
- `fields` is a list of fields that are contained in the section. Any fields above can be used in this parameter to create a section with fields inside of it

```json
{
      "section": "Main",
      "simple_name": "main",
      "fields": [],
  },
```

An example section is below:

![section](./images/formatting_season_fields/section.png)

```json
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
    ],
},
```

