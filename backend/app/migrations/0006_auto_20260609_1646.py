from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0005_auto_20260607_2033')]

    initial = False

    operations = [
        ops.AddField(
            model_name='Profile',
            name='created_at',
            field=fields.DatetimeField(null=True, auto_now=False, auto_now_add=True),
        ),
        ops.AddField(
            model_name='User',
            name='email_verified',
            field=fields.BooleanField(default=False, db_default=False),
        ),
    ]
