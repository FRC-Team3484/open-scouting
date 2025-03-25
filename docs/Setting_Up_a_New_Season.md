# Setting Up a New Season

This page documents which steps should be followed at the start of a season to quickly prepare Open Scouting for a new game

These steps should be followed as early in the season as possible, preferably on kickoff day, and at the very least before Week 0 begins

## 1. Update `season_fields.py`
- Add a new year to the `season_fields.py` file. Follow [Formatting Season Fields](./Formatting_Season_Fields.md) for how to do this. Data entries should be kept simple and not complicated, simplify or remove any fields that you can, and the very minimum amount of fields should be kept required, the goal is to make the process as easy and quick as possible for scouts.
- Add the new year to the mapping dictionary in the `get_season_fields` function

## 2. Update `pit_scouting_questions.py`
- Add a new year to the `pit_scouting_questions.py` file. Follow [Formatting Pit Scouting Questions](./Formatting_Pit_Scouting_Questions.md) for how to do this. Simplify the amount of hte questions for scouts to ask to make the pit scouting process as easy as possible.
- This step is optional, simply creating an empty list in the `pit_scouting_questions.py` file will work, however scouts will have to manually enter in all of the questions as custom questions when they scout

## 3. Update `views.py` and `models.py`
- Navigate to `/main/views.py`
  - Add the new year to the `YEARS` array
  - Add to the `get_demo_data_from_year` function to return the new year's data
- Navigate to `/main/models.py`
  - Add the new year to the `YEARS` array as a tuple, just match with the years that are already in this array

## 4. Create demo data
- Follow the instructions in [Creating Demonstration Data](./Creating_Demonstration_Data.md) for how to do this

Open Scouting should now be updated to the new season! You should navigate around and ensure that everything is working as expected