from telegram import User, Chat

from django.db import models
from django.apps import apps


class TelegramUserQuerySet(models.QuerySet):
    """
    QuerySet for TelegramUserManager
    """

    pass


class TelegramUserManagerBase(models.Manager):
    """
    Manager for TelegramUser
    """

    async def aget_or_create_from_telegram_user(self, tg_user: User):
        """
        Get or create a TelegramUser object from telegram.User.
        """
        user, _ = await self.aget_or_create(
            telegram_id=tg_user.id,
            defaults={
                "username": tg_user.username,
                "first_name": tg_user.first_name,
                "last_name": tg_user.last_name,
                "language_code": tg_user.language_code,
                "is_bot": tg_user.is_bot,
            },
        )
        return user


TelegramUserManager = TelegramUserManagerBase.from_queryset(TelegramUserQuerySet)


class TelegramChatQuerySet(models.QuerySet):
    """
    QuerySet for TelegramChatManager
    """

    pass


class TelegramChatManagerBase(models.Manager):
    """
    Manager for TelegramChat
    """

    async def aget_or_create_from_telegram_chat(self, tg_chat: Chat):
        """
        Get or create a TelegramChat object from telegram.Chat.
        """

        chat, _ = await self.aget_or_create(
            telegram_id=tg_chat.id,
            defaults={
                "chat_type": tg_chat.type,
                "title": tg_chat.title,
                "username": tg_chat.username,
            },
        )
        return chat


TelegramChatManager = TelegramChatManagerBase.from_queryset(TelegramChatQuerySet)


class TelegramGroupMemberQuerySet(models.QuerySet):
    """
    QuerySet for TelegramGroupMemberManager
    """

    pass


class TelegramGroupMemberManagerBase(models.Manager):
    """
    Manager for TelegramGroupMember
    """

    async def ensure_membership(
        self,
        user,
        chat,
        role="member",
    ):
        await self.aupdate_or_create(
            user=user,
            chat=chat,
            defaults={
                "role": role,
                "is_active": True,
                "left_at": None,
            },
        )


TelegramGroupMemberManager = TelegramGroupMemberManagerBase.from_queryset(
    TelegramGroupMemberQuerySet
)
