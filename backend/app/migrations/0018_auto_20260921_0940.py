from tortoise import migrations
from tortoise.migrations import operations as ops
from ..models import FieldType, ScoutingType, StatType
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0017_auto_20260719_1533')]

    initial = False

    operations = [  # pyright: ignore[reportAssignmentType]
        ops.CreateModel(
            name='FieldChoice',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('name', fields.CharField(max_length=255)),
                ('simple_name', fields.CharField(max_length=255)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('created_by', fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL)),
            ],
            options={'table': 'fieldchoice', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'A model for choices in fields'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='FieldOptions',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('choices', fields.ManyToManyField('models.FieldChoice', null=True, unique=True, db_constraint=True, through='fieldoptions_fieldchoice', forward_key='fieldchoice_id', backward_key='fieldoptions_id', related_name='field_options', on_delete=OnDelete.SET_NULL)),
                ('default', fields.IntField(null=True)),
                ('minimum', fields.IntField(null=True)),
                ('maximum', fields.IntField(null=True)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('created_by', fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL)),
            ],
            options={'table': 'fieldoptions', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'A model for options in fields'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='ScoutingField',
            fields=[  # pyright: ignore[reportArgumentType]
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('season', fields.ForeignKeyField('models.Season', source_field='season_id', null=True, db_constraint=True, to_field='uuid', related_name='scouting_fields', on_delete=OnDelete.SET_NULL)),
                ('organization', fields.ForeignKeyField('models.Organization', source_field='organization_id', null=True, db_constraint=True, to_field='uuid', related_name='fields', on_delete=OnDelete.CASCADE)),
                ('parent', fields.ForeignKeyField('models.ScoutingField', source_field='parent_id', null=True, db_constraint=True, to_field='uuid', related_name='children', on_delete=OnDelete.SET_NULL)),
                ('name', fields.CharField(max_length=255)),
                ('description', fields.CharField(null=True, max_length=255)),
                ('scouting_type', fields.CharEnumField(description='MATCH: match\nPIT: pit', enum_type=ScoutingType, max_length=5)),
                ('field_type', fields.CharEnumField(description='SECTION: section\nSTRING: string\nLARGE_NUMBER: large_number\nSMALL_NUMBER: small_number\nCOARSE_SMALL_NUMBER: coarse_small_number\nBOOLEAN: boolean\nCHOICE: choice\nMULTIPLE_CHOICE: multiple_choice\nNUMBER: number', enum_type=FieldType, max_length=19)),
                ('stat_type', fields.CharEnumField(null=True, description='SECTION: section\nAUTON_SCORE: auton_score\nAUTON_MISS: auton_miss\nTELEOP_SCORE: teleop_score\nTELEOP_MISS: teleop_miss\nCAPABILITY: capability\nOTHER: other\nIGNORE: ignore', enum_type=StatType, max_length=12)),
                ('game_piece', fields.ForeignKeyField('models.GamePiece', source_field='game_piece_id', null=True, db_constraint=True, to_field='uuid', related_name='scouting_fields', on_delete=OnDelete.SET_NULL)),
                ('required', fields.BooleanField(default=False)),
                ('options', fields.ForeignKeyField('models.FieldOptions', source_field='options_id', null=True, db_constraint=True, to_field='uuid', related_name='scouting_fields', on_delete=OnDelete.SET_NULL)),
                ('order', fields.IntField(default=0)),
                ('archived', fields.BooleanField(default=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('created_by', fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL)),
            ],
            options={'table': 'scoutingfield', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Generic model for both match and pit scouting fields'},
            bases=['Model'],
        ),
    ]
