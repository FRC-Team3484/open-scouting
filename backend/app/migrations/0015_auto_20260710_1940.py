from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0014_auto_20260704_1628')]

    initial = False

    operations = [
        ops.AddField(
            model_name='Event',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='GamePiece',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='MatchScoutingAnswer',
            name='created_at',
            field=fields.DatetimeField(null=True, auto_now=False, auto_now_add=True),
        ),
        ops.AddField(
            model_name='MatchScoutingAnswer',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='MatchScoutingField',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='MatchScoutingSubmission',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='Organization',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='OrganizationMember',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='Passkey',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='PitScoutingAnswer',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='PitScoutingField',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='Profile',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='Season',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='Settings',
            name='created_at',
            field=fields.DatetimeField(null=True, auto_now=False, auto_now_add=True),
        ),
        ops.AddField(
            model_name='Settings',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='TeamPit',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='User',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AddField(
            model_name='VerificationCode',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
        ops.AlterModelOptions(
            name='WebAuthnChallenge',
            options={'table': 'webauthnchallenge', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Store a webauthn challenge for a user'},
        ),
        ops.AddField(
            model_name='WebAuthnChallenge',
            name='created_at',
            field=fields.DatetimeField(null=True, auto_now=False, auto_now_add=True),
        ),
        ops.AddField(
            model_name='WebAuthnChallenge',
            name='created_by',
            field=fields.ForeignKeyField('models.Session', source_field='created_by_id', null=True, db_constraint=True, to_field='uuid', related_name=False, on_delete=OnDelete.CASCADE),
        ),
    ]
