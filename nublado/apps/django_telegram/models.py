from telegram.constants import ChatType, ChatMemberStatus

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from core.models import TimestampModel
from .managers import (
    TelegramUserManager,
    TelegramChatManager,
    TelegramGroupMemberManager,
)


class TelegramUser(TimestampModel):
    """
    Represents a Telegram user.

    Data ownership:
    - telegram_id: authoritative (Telegram)
    - username / names / language: cached snapshot (Telegram-owned, DB-cached)
    - is_bot: cached snapshot, used for bot-side logic (e.g. karma blocking)

    This model exists to provide stable identity and historical continuity
    even if Telegram-side data changes or disappears.
    """

    telegram_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    language_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        default=settings.LANGUAGE_CODE,
    )
    is_bot = models.BooleanField(default=False)

    objects = TelegramUserManager()

    def __str__(self):
        # In case username doesn't exist, just return the id.
        return self.username or str(self.telegram_id)


class TelegramChat(TimestampModel):
    """
    Represents a Telegram chat (private, group, supergroup, channel).

    Data ownership:
    - telegram_id: authoritative (Telegram)
    - chat_type: authoritative (Telegram)
    - title / username: cached snapshot (Telegram-owned)

    This model exists to anchor group-scoped features such as
    memberships, points, and settings.
    """

    class TelegramChatType(models.TextChoices):
        PRIVATE = ChatType.PRIVATE, _("private")
        GROUP = ChatType.GROUP, _("group")
        SUPERGROUP = ChatType.SUPERGROUP, _("supergroup")
        CHANNEL = ChatType.CHANNEL, _("channel")

    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    chat_type = models.CharField(max_length=20, choices=TelegramChatType)
    title = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    objects = TelegramChatManager()

    def __str__(self):
        return f"{self.chat_type}:{self.telegram_id}"


class TelegramGroupMember(TimestampModel):
    """
    Represents a user's membership in a specific Telegram chat.

    Data ownership:
    - user / chat: authoritative relational links
    - role: cached snapshot of last known Telegram role (NOT authoritative)
    - is_active / joined_at / left_at: authoritative (application-owned)
    - points: authoritative (application-owned gamification state)

    This model is the core domain entity for per-group features.
    """

    class GroupRole(models.TextChoices):
        MEMBER = ChatMemberStatus.MEMBER, _("member")
        ADMIN = ChatMemberStatus.ADMINISTRATOR, _("admin")
        OWNER = ChatMemberStatus.OWNER, _("owner")

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

    # Cached snapshot — never authoritative for permissions
    role = models.CharField(max_length=20, choices=GroupRole)

    # Application-owned membership state
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    # Gamification (application-owned)
    points = models.IntegerField(default=0)

    objects = TelegramGroupMemberManager()

    class Meta:
        unique_together = ("user", "chat")
        indexes = [
            models.Index(fields=["chat", "-points"]),
        ]

    def __str__(self):
        return f"{self.user} in {self.chat} ({self.role})"
