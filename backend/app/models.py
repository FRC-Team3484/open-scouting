from tortoise import fields
from tortoise.models import Model

# Authentication
class User(Model):
    uuid = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Profile(Model):
    uuid = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="profiles")
    display_name = fields.CharField(max_length=255)
    team_number = fields.IntField(null=True)

    def __str__(self):
        return self.user

class Organization(Model):
    uuid = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255, null=False)
    label = fields.CharField(max_length=512)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

class OrganizationMember(Model):
    uuid = fields.UUIDField(pk=True)
    organization = fields.ForeignKeyField("models.Organization", related_name="members")
    user = fields.ForeignKeyField("models.User", related_name="organizations")
    role = fields.CharField(max_length=255) # member, admin
    created_at = fields.DatetimeField(auto_now_add=True)

# Main
class Season(Model):
    uuid = fields.UUIDField(pk=True)
    year = fields.IntField()
    label = fields.CharField(max_length=255)
    active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    # Deactivate all other seasons if this one is saved as active
    async def save(self, *args, **kwargs):
        if self.active:
            await Season.filter(active=True).exclude(uuid=self.uuid).update(active=False)

        await super().save(*args, **kwargs)

