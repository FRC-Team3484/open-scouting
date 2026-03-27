from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0002_auto_20260313_1732')]

    initial = False

    operations = [
        ops.AddField(
            model_name='PitScoutingField',
            name='required',
            field=fields.BooleanField(null=True),
        ),
        ops.RunSQL(
            "UPDATE pitscoutingfield SET required = false WHERE required IS NULL;",
            ""
        )
    ]
