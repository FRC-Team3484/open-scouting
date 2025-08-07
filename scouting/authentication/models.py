from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    display_name = models.CharField(max_length=999, verbose_name=_("Display Name"))
    team_number = models.CharField(max_length=6, verbose_name=_("Team Number"))

    def __str__(self):
        return f"{self.user.username}'s profile"


class VerificationCode(models.Model):
    code = models.CharField(max_length=6, verbose_name=_("Verification Code"))
    created = models.DateTimeField(null=True, blank=True, verbose_name=_("Created"))
    expires = models.DateTimeField(null=True, blank=True, verbose_name=_("Expires"))
    user_uuid = models.UUIDField(null=True, blank=True, verbose_name=_("User UUID"))
    verified = models.BooleanField(default=False, verbose_name=_("Verified"))

    def __str__(self):
        if self.verified:
            return f"[Verified] Verification code for user {self.user_uuid}"
        else:
            return f"[Unverified] Verification code for user {self.user_uuid}"


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    favorite_events = models.JSONField(
        default=list,
        blank=True,
        editable=False,
        verbose_name=_("Favorite Events"),
        help_text=_(
            "The user's favorite events, pinned to the top of their event list"
        ),
    )

    def __str__(self):
        return f"Settings for {self.user.username}"

    class Meta:
        verbose_name_plural = _("Settings")
