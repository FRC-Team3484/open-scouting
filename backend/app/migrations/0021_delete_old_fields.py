from typing import TYPE_CHECKING, cast

from tortoise import migrations
from tortoise.migrations.schema_editor.base import BaseSchemaEditor
from tortoise.migrations.schema_generator.state_apps import StateApps
from tortoise.migrations import operations as ops

if TYPE_CHECKING:
    from ..datatypes import MatchScoutingFieldType
    from ..datatypes import PitScoutingFieldType


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

    match_scouting_fields: list["MatchScoutingFieldType"] = await MatchScoutingField.all()
    pit_scouting_fields: list["PitScoutingFieldType"] = await PitScoutingField.all()

    # Delete old fields
    for field in match_scouting_fields:
        await field.delete()
    for field in pit_scouting_fields:
        await field.delete()

    print(f"\nMigration: Deleted {len(match_scouting_fields)} MatchScoutingFields")
    print(f"Migration: Deleted {len(pit_scouting_fields)} PitScoutingFields")

class Migration(migrations.Migration):
    dependencies = [
        ('models', '0020_update_answer_keys'),
    ]

    initial = False

    operations = [
        migrations.RunPython(forwards, None, atomic=True),
        ops.RemoveField("MatchScoutingField", "parent"),
        ops.DeleteModel('MatchScoutingField'),
        ops.DeleteModel('PitScoutingField'),
    ]