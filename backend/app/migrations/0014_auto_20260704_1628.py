from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0013_auto_20260704_1207')]

    initial = False

    operations = [
        ops.AddField(
            model_name='Passkey',
            name='label',
            field=fields.CharField(null=True, max_length=255),
        ),
    ]
