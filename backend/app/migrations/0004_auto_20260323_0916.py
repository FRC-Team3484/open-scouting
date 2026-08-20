from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0003_auto_20260323_0913')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='PitScoutingField',
            name='required',
            field=fields.BooleanField(default=False),
        ),
    ]
