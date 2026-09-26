from typing import TYPE_CHECKING, cast

from tortoise import migrations
from tortoise.exceptions import ValidationError
from tortoise.migrations.schema_editor.base import BaseSchemaEditor
from tortoise.migrations.schema_generator.state_apps import StateApps

from ..models import FieldType, StatType

if TYPE_CHECKING:
    from ..datatypes import MatchScoutingFieldType
    from ..datatypes import PitScoutingFieldType
    from ..models import FieldChoice as FieldChoiceType
    from ..models import FieldOptions as FieldOptionsType
    from ..models import ScoutingField as ScoutingFieldType


async def forwards(apps: StateApps, schema_editor: BaseSchemaEditor) -> None:
    """
    Transforms all MatchScoutingField and PitScoutingField to the new ScoutingField model

    For each MatchScoutingField and PitScoutingField, with options, create corresponding FieldOptions and FieldChoice as needed
    """
    # Get models
    MatchScoutingField: type["MatchScoutingFieldType"] = cast(
        type["MatchScoutingFieldType"], 
        apps.get_model('models', 'MatchScoutingField')
    )
    PitScoutingField: type["PitScoutingFieldType"] = cast(
        type["PitScoutingFieldType"], 
        apps.get_model('models', 'PitScoutingField')
    )

    FieldChoice: type["FieldChoiceType"] = cast(
        type["FieldChoiceType"], 
        apps.get_model('models', 'FieldChoice')
    )
    FieldOptions: type["FieldOptionsType"] = cast(
        type["FieldOptionsType"], 
        apps.get_model('models', 'FieldOptions')
    )
    ScoutingField: type["ScoutingFieldType"] = cast(
        type["ScoutingFieldType"], 
        apps.get_model('models', 'ScoutingField')
    )

    new_match_scouting_fields: list["ScoutingFieldType"] = []
    new_pit_scouting_fields: list["ScoutingFieldType"] = []

    # Transform MatchScoutingField 
    match_scouting_fields: list["MatchScoutingFieldType"] = await MatchScoutingField.all()
    for field in match_scouting_fields:
        options: "FieldOptionsType | None" = None
        choices: list["FieldChoiceType"] = []

        # Validate field_type and stat_type
        field_type: FieldType | None = None
        stat_type: StatType | None = None

        try:
            field_type = FieldType(field.field_type)
            stat_type = (StatType(field.stat_type) if field.stat_type else None)
        except ValueError:
            raise ValidationError(f"Invalid field_type ({field.field_type}) or stat_type ({field.stat_type}) for field {field.name} ({field.uuid})")

        # Validate options, if applicable
        if field_type in [FieldType.CHOICE, FieldType.MULTIPLE_CHOICE, FieldType.SMALL_NUMBER, FieldType.COARSE_SMALL_NUMBER]:
            # Field should have options
            if field.options and field.options != {} and field.options != []: # Some legacy fields have options set to [] as default
                # Field does have options
                if field_type in [FieldType.CHOICE, FieldType.MULTIPLE_CHOICE]:
                    # Field should have choice options
                    if field.options.get("choices") and field.options.get("choices") != []:
                        # Field has choice options
                        for choice in field.options.get("choices", []):
                            if not choice.get("id") or not choice.get("name"):
                                print(f"Migration warning: Choice for field {field.name} ({field.uuid}) has no ID or name: {choice}")
                                continue

                            new_choice: "FieldChoiceType" = FieldChoice(
                                uuid=choice.get("id"),
                                name=choice.get("name"),
                                simple_name=choice.get("name").lower().replace(" ", "_"),
                            )
                            await new_choice.save()
                            choices.append(new_choice)

                    options = FieldOptions()
                    await options.save()
                    await options.choices.add(*choices)

                elif field_type in [FieldType.SMALL_NUMBER, FieldType.COARSE_SMALL_NUMBER]:
                    # Field should have number options
                    if field.options.get("default") is not None or field.options.get("minimum") is not None or field.options.get("maximum") is not None:
                        # Field has number options
                        options = FieldOptions(
                            default=field.options.get("default", 0),
                            minimum=field.options.get("minimum", 0),
                            maximum=field.options.get("maximum", 0),
                        )
                        await options.save()
                    else:
                        # Field is missing number options, using defaults
                        options = FieldOptions(
                            default=0,
                            minimum=0,
                            maximum=0,
                        )
                        await options.save()
            else:
                # Field doesn't have options, using defaults
                options = FieldOptions()
                await options.save()

        new_field: "ScoutingFieldType" = ScoutingField(
            uuid=field.uuid,
            season_id=field.season_id,
            organization_id=field.organization_id,
            parent_id=None, # None for now, and will be restored once all fields are in the database to handle foreign key constraints
            name=field.name,
            description=field.description,
            scouting_type="match",
            field_type=field_type,
            stat_type=stat_type,
            game_piece_id=field.game_piece_id,
            required=field.required,
            options_id=options.uuid if options else None,
            order=field.order,
            archived=field.archived,
            created_at=field.created_at,
            created_by_id=field.created_by_id,
        )
        new_match_scouting_fields.append(new_field)
        await new_field.save()

    # Restore parent_id
    for field in match_scouting_fields:
        if field.parent_id is not None:
            await ScoutingField.filter(uuid=field.uuid).update(
                parent_id=field.parent_id
            )

    # Print MatchScoutingField migration results
    print(f"Migration: Migrated {len(new_match_scouting_fields)} MatchScoutingFields")
    if len(match_scouting_fields) != len(new_match_scouting_fields):
        print(f"Migration warning: {len(match_scouting_fields) - len(new_match_scouting_fields)} MatchScoutingFields were not migrated")
    
    # Transform PitScoutingField
    pit_scouting_fields: list["PitScoutingFieldType"] = await PitScoutingField.all()
    for field in pit_scouting_fields:
        options: "FieldOptionsType | None" = None
        choices: list["FieldChoiceType"] = []

        # Validate field_type
        try:
            # Handle pit field_type text to string migration
            if field.field_type == "text":
                field_type = FieldType.STRING
            else:
                field_type = FieldType(field.field_type)
        except ValueError:
            raise ValidationError(f"Field type ({field.field_type}) for field {field.name} ({field.uuid}) is invalid")

        # Validate options, if applicable
        if field_type == FieldType.CHOICE:
            # Field should have options
            if field.options and field.options != {} and field.options != []: # Some legacy fields have options set to [] as default
                # Field does have options
                for choice in field.options.get("choices", []):
                    if not choice.get("id") or not choice.get("name"):
                        print(f"Migration warning: Choice for field {field.name} ({field.uuid}) has no ID or name: {choice}")
                        continue

                    new_choice: "FieldChoiceType" = FieldChoice(
                        uuid=choice.get("id"),
                        name=choice.get("name"),
                        simple_name=choice.get("name").lower().replace(" ", "_"),
                    )
                    await new_choice.save()
                    choices.append(new_choice)

                options = FieldOptions()
                await options.save()
                await options.choices.add(*choices)
            else:
                # Field doesn't have options, using defaults
                options = FieldOptions()
                await options.save()

        new_field: "ScoutingFieldType" = ScoutingField(
            uuid=field.uuid,
            season_id=field.season_id,
            organization_id=field.organization_id,
            name=field.name,
            description=field.description,
            scouting_type="pit",
            field_type=field_type,
            required=field.required,
            options_id=options.uuid if options else None,
            order=field.order,
            archived=field.archived,
            created_at=field.created_at,
            created_by_id=field.created_by_id,
        )
        new_pit_scouting_fields.append(new_field)
        await new_field.save()

    # Print PitScoutingField migration results
    print(f"Migration: Migrated {len(new_pit_scouting_fields)} PitScoutingFields")
    if len(pit_scouting_fields) != len(new_pit_scouting_fields):
        print(f"Migration warning: {len(pit_scouting_fields) - len(new_pit_scouting_fields)} PitScoutingFields were not migrated")

    print("\nField migration complete")

class Migration(migrations.Migration):
    dependencies = [
        ('models', '0018_auto_20260921_0940'),
    ]

    initial = False

    operations = [
        migrations.RunPython(forwards, None, atomic=True),
    ]