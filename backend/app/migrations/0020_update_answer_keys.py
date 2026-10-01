from tortoise import migrations
from tortoise.migrations import operations as ops
from app.models import FieldType
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0019_migrate_old_fields')]

    initial = False

    operations = [
        ops.RunSQL(
            sql="""
                ALTER TABLE matchscoutinganswer
                DROP CONSTRAINT IF EXISTS matchscoutinganswer_field_id_fkey;

                ALTER TABLE matchscoutinganswer
                ADD CONSTRAINT matchscoutinganswer_field_id_fkey
                FOREIGN KEY (field_id)
                REFERENCES scoutingfield(uuid)
                ON DELETE SET NULL;

                ALTER TABLE pitscoutinganswer
                DROP CONSTRAINT IF EXISTS pitscoutinganswer_field_id_fkey;

                ALTER TABLE pitscoutinganswer
                ADD CONSTRAINT pitscoutinganswer_field_id_fkey
                FOREIGN KEY (field_id)
                REFERENCES scoutingfield(uuid)
                ON DELETE SET NULL;
            """,
            reverse_sql="""
                ALTER TABLE matchscoutinganswer
                DROP CONSTRAINT IF EXISTS matchscoutinganswer_field_id_fkey;

                ALTER TABLE matchscoutinganswer
                ADD CONSTRAINT matchscoutinganswer_field_id_fkey
                FOREIGN KEY (field_id)
                REFERENCES matchscoutingfield(uuid)
                ON DELETE CASCADE;

                ALTER TABLE pitscoutinganswer
                DROP CONSTRAINT IF EXISTS pitscoutinganswer_field_id_fkey;

                ALTER TABLE pitscoutinganswer
                ADD CONSTRAINT pitscoutinganswer_field_id_fkey
                FOREIGN KEY (field_id)
                REFERENCES pitscoutingfield(uuid)
                ON DELETE CASCADE;
            """,
        ),
        ops.AlterField(
            model_name='ScoutingField',
            name='field_type',
            field=fields.CharEnumField(description='SECTION: section\nSTRING: string\nLARGE_NUMBER: large_number\nSMALL_NUMBER: small_number\nCOARSE_SMALL_NUMBER: coarse_small_number\nBOOLEAN: boolean\nCHOICE: choice\nMULTIPLE_CHOICE: multiple_choice\nNUMBER: number\nIMAGE: image', enum_type=FieldType, max_length=19),
        ),
        ops.AlterField(
            model_name="MatchScoutingAnswer",
            name="field",
            field=fields.ForeignKeyField("models.ScoutingField", source_field="field_id", null=True, db_constraint=True, to_field="uuid", related_name="match_scouting_answers", on_delete=fields.SET_NULL),
        ),
        ops.AlterField(
            model_name="PitScoutingAnswer",
            name="field",
            field=fields.ForeignKeyField("models.ScoutingField", source_field="field_id", null=True, db_constraint=True, to_field="uuid", related_name="pit_scouting_answers", on_delete=fields.SET_NULL),
        )
    ]
