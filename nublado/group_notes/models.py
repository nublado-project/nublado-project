from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import TimestampModel
from .managers import GroupNoteManager


class GroupNote(TimestampModel):
    group_id = models.BigIntegerField()
    note_tag = models.CharField(
        max_length=255
    )
    # Reference to a Telegram message
    message_id = models.BigIntegerField(
        null=True
    )
    objects = GroupNoteManager()

    class Meta:
        verbose_name = _("Group note")
        verbose_name_plural = _("Group notes")
        unique_together = ('group_id', 'note_tag')

    def __str__(self):
        return '{0} : {1}'.format(self.group_id, self.note_tag)