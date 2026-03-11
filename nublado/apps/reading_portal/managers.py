from django.db import models

from django_telegram.models import TelegramChat


class ReadingPortalQuerySet(models.QuerySet):
    """
    QuerySet for ReadingPortalManager
    """

    def draft_status(self):
        return self.filter(portal_status=self.model.PortalStatus.DRAFT)

    def open_status(self):
        return self.filter(portal_status=self.model.PortalStatus.OPEN)


class ReadingPortalManager(models.Manager.from_queryset(ReadingPortalQuerySet)):
    """
    Manager for ReadingPortal
    """

    async def aget_open(self, chat: TelegramChat):
        return await (
            self.get_queryset()
            .select_related("chat")
            .prefetch_related("portal_readings")
            .open_status()
            .aget(chat=chat)
        )

    async def anext_draft(self, chat: TelegramChat):
        return await (
            self.get_queryset()
            .select_related("chat")
            .prefetch_related("portal_readings")
            .draft_status()
            .filter(chat=chat)
            .order_by("date_created")
            .afirst()
        )
