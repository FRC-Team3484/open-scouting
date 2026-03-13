from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from tortoise import fields

class Migration(migrations.Migration):
    dependencies = [('models', '0001_initial')]

    initial = False

    operations = [
        ops.AlterField(
            model_name='MatchScoutingSubmission',
            name='user',
            field=fields.ForeignKeyField('models.User', source_field='user_id', null=True, db_constraint=True, to_field='uuid', related_name='answers', on_delete=OnDelete.CASCADE),
        ),
    ]
