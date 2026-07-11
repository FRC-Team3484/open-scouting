from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0015_auto_20260710_1940')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='Event',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='Event',
            name='season',
            field=fields.ForeignKeyField('models.Season', source_field='season_id', null=True, db_constraint=True, to_field='uuid', related_name='events', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='GamePiece',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='GamePiece',
            name='season',
            field=fields.ForeignKeyField('models.Season', source_field='season_id', null=True, db_constraint=True, to_field='uuid', related_name='game_pieces', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='MatchScoutingAnswer',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='MatchScoutingAnswer',
            name='field',
            field=fields.ForeignKeyField('models.MatchScoutingField', source_field='field_id', null=True, db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='MatchScoutingAnswer',
            name='submission',
            field=fields.ForeignKeyField('models.MatchScoutingSubmission', source_field='submission_id', null=True, db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='MatchScoutingField',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='MatchScoutingField',
            name='game_piece',
            field=fields.ForeignKeyField('models.GamePiece', source_field='game_piece_id', null=True, db_constraint=True, to_field='uuid', related_name='fields', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='MatchScoutingField',
            name='parent',
            field=fields.ForeignKeyField('models.MatchScoutingField', source_field='parent_id', null=True, db_constraint=True, to_field='uuid', related_name='children', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='MatchScoutingField',
            name='season',
            field=fields.ForeignKeyField('models.Season', source_field='season_id', null=True, db_constraint=True, to_field='uuid', related_name='fields', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='MatchScoutingSubmission',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='MatchScoutingSubmission',
            name='event',
            field=fields.ForeignKeyField('models.Event', source_field='event_id', null=True, db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.SET_NULL),
        ),
        ops.RemoveField(model_name='MatchScoutingSubmission', name='user'),
        ops.AlterField(
            model_name='Organization',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='OrganizationMember',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='Passkey',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='PitScoutingAnswer',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='PitScoutingAnswer',
            name='field',
            field=fields.ForeignKeyField('models.PitScoutingField', source_field='field_id', null=True, db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='PitScoutingAnswer',
            name='team',
            field=fields.ForeignKeyField('models.TeamPit', source_field='team_id', null=True, db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='PitScoutingField',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='PitScoutingField',
            name='season',
            field=fields.ForeignKeyField('models.Season', source_field='season_id', null=True, db_constraint=True, to_field='uuid', related_name='pit_fields', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='Profile',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='Season',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='Session',
            name='user',
            field=fields.ForeignKeyField('models.User', source_field='user_id', null=True, db_constraint=True, to_field='uuid', related_name='sessions', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='Settings',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='TeamPit',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='TeamPit',
            name='event',
            field=fields.ForeignKeyField('models.Event', source_field='event_id', null=True, db_constraint=True, to_field='uuid', related_name='team_pits', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='TeamPit',
            name='season',
            field=fields.ForeignKeyField('models.Season', source_field='season_id', null=True, db_constraint=True, to_field='uuid', related_name='team_pits', on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='User',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='VerificationCode',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
        ops.AlterField(
            model_name='WebAuthnChallenge',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.SET_NULL),
        ),
    ]
