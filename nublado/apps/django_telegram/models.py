from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimestampModel
from .managers import (
    TelegramUserManager,
    TelegramChatManager,
    TelegramGroupMemberManager,
)


class TelegramUser(TimestampModel):

    telegram_id = models.BigIntegerField(unique=True, primary_key=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(max_length=10, null=True, blank=True)
    is_bot = models.BooleanField(default=False)

    objects = TelegramUserManager()

    def __str__(self):
        return f"{self.telegram_id} (@{self.username})"


class TelegramChat(TimestampModel):

    class ChatType(models.TextChoices):
        PRIVATE = "private", _("private")
        GROUP = "group", _("group")
        SUPERGROUP = "supergroup", _("supergroup")
        CHANNEL = "channel", _("channel")

    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    chat_type = models.CharField(max_length=20, choices=ChatType)
    title = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    objects = TelegramChatManager()

    def __str__(self):
        return f"{self.chat_type}:{self.telegram_id}"


class TelegramGroupMember(TimestampModel):

    class GroupRole(models.TextChoices):
        MEMBER = "member", _("member")
        ADMIN = "admin", _("admin")
        OWNER = "owner", _("owner")

    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    chat = models.ForeignKey(
        TelegramChat,
        on_delete=models.CASCADE,
        related_name="members",
    )
    role = models.CharField(max_length=20, choices=GroupRole)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    objects = TelegramGroupMemberManager()

    class Meta:
        unique_together = ("user", "chat")

    def __str__(self):
        return f"{self.user} in {self.chat} ({self.role})"
