from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from core.models import TimestampModel, UUIDModel
from .managers import (
    BotConfigManager,
    GroupMemberManager,
)


class BotConfig(TimestampModel):
    LANGUAGE_CHOICES = settings.LANGUAGES

    id = models.TextField(
        primary_key=True,
        editable=False
    )

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=settings.EN,
    )

    objects = BotConfigManager()

    class Meta:
        verbose_name = _("Bot configuration")


class GroupMember(TimestampModel, UUIDModel):
    user_id = models.PositiveBigIntegerField()
    group_id = models.BigIntegerField()
    points = models.PositiveBigIntegerField(
        default=0
    )
    point_increment = models.PositiveBigIntegerField(
        default=1
    )

    objects = GroupMemberManager()

    class Meta:
        unique_together = ('user_id', 'group_id')

    def __str__(self):
        return "group: {0}, user: {1}".format(
            self.group_id,
            self.user_id
        )