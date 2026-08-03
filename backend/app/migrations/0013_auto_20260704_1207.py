from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0012_auto_20260704_1206')]

    initial = False

    operations = [
        ops.AddField(
            model_name='WebAuthnChallenge',
            name='challenge',
            field=fields.BinaryField(null=True),
        ),
    ]
