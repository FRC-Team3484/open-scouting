from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=999)
    team_number = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.user.username}'s profile"


class VerificationCode(models.Model):
    code = models.CharField(max_length=6)
    created = models.DateTimeField(null=True, blank=True)
    expires = models.DateTimeField(null=True, blank=True)
    user_uuid = models.UUIDField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        if self.verified:
            return f"[Verified] Verification code for user {self.user_uuid}"
        else:
            return f"[Unverified] Verification code for user {self.user_uuid}"


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_events = models.JSONField(
        default=list,
        blank=True,
        editable=False,
        verbose_name="Favorite Events",
        help_text="The user's favorite events, pinned to the top of their event list",
    )

    def __str__(self):
        return f"Settings for {self.user.username}"

    class Meta:
        verbose_name_plural = "Settings"
