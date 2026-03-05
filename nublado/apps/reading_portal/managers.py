from django.db import models

from django_telegram.models import TelegramChat


class ReadingPortalQuerySet(models.QuerySet):
    """
    QuerySet for ReadingPortalManager
    """

class ReadingPortalManager(models.Manager.from_queryset(ReadingPortalQuerySet)):
    """
    Manager for ReadingPortal
    """

    async def aget_draft(self, chat: TelegramChat):
        return await (
            self.get_queryset()
            .aget(
                chat=chat,
                portal_status=ReadingPortal.PortalStatus.DRAFT
            )
        )

    async def aget_open(self, chat: TelegramChat):
        return await (
            self.get_queryset().
            aget(
                chat=chat,
                portal_status=ReadingPortal.PortalStatus.OPEN
            )
        )