from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    display_name = fields.CharField(max_length=255)
    hashed_password = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username
