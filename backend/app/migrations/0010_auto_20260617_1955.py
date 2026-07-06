from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0009_auto_20260613_2003')]

    initial = False

    operations = [
        ops.CreateModel(
            name='VerificationCode',
            fields=[
                ('uuid', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('user', fields.ForeignKeyField('models.User', source_field='user_id', null=True, db_constraint=True, to_field='uuid', related_name='verification_codes', on_delete=OnDelete.CASCADE)),
                ('code', fields.CharField(max_length=6)),
                ('email', fields.CharField(max_length=255)),
                ('verified', fields.BooleanField(default=False)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
            ],
            options={'table': 'verificationcode', 'app': 'models', 'pk_attr': 'uuid', 'table_description': 'Defines a verification code for a user, used to verify their email or change their password'},
            bases=['Model'],
        ),
    ]
