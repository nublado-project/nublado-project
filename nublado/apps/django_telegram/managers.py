from telegram import User, Chat

from django.db import models


class TelegramUserQuerySet(models.QuerySet):
    """
    QuerySet for TelegramUserManager
    """


class TelegramUserManagerBase(models.Manager):
    """
    Manager for TelegramUser
    """

    async def aget_or_create_from_telegram_user(self, tg_user: User):
        """
        Get or create a TelegramUser object from telegram.User.
        """
        user, created = await self.aget_or_create(
            telegram_id=tg_user.id,
            defaults={
                "username": tg_user.username,
                "first_name": tg_user.first_name,
                "last_name": tg_user.last_name,
                "is_bot": tg_user.is_bot,
            },
        )
        if not created:
            # Update snapshot fields in db.
            updated_fields = []

            if user.username != tg_user.username:
                user.username = tg_user.username
                updated_fields.append("username")

            if user.first_name != tg_user.first_name:
                user.first_name = tg_user.first_name
                updated_fields.append("first_name")

            if user.last_name != tg_user.last_name:
                user.last_name = tg_user.last_name
                updated_fields.append("last_name")

            if user.is_bot != tg_user.is_bot:
                user.is_bot = tg_user.is_bot
                updated_fields.append("is_bot")

            if updated_fields:
                await user.asave(update_fields=updated_fields)

        return user


TelegramUserManager = TelegramUserManagerBase.from_queryset(TelegramUserQuerySet)


class TelegramChatQuerySet(models.QuerySet):
    """
    QuerySet for TelegramChatManager
    """


class TelegramChatManagerBase(models.Manager):
    """
    Manager for TelegramChat
    """

    async def aget_or_create_from_telegram_chat(self, tg_chat: Chat):
        """
        Get or create a TelegramChat object from telegram.Chat.
        """

        chat, created = await self.aget_or_create(
            telegram_id=tg_chat.id,
            defaults={
                "chat_type": tg_chat.type,
                "title": tg_chat.title,
                "username": tg_chat.username,
            },
        )
        if not created:
            # Update snapshot fields in db.
            updated_fields = []

            if chat.chat_type != tg_chat.type:
                chat.chat_type = tg_chat.type
                updated_fields.append("chat_type")

            if chat.title != tg_chat.title:
                chat.title = tg_chat.title
                updated_fields.append("title")

            if chat.username != tg_chat.username:
                chat.username = tg_chat.username
                updated_fields.append("username")

            if updated_fields:
                await chat.asave(update_fields=updated_fields)
        return chat


TelegramChatManager = TelegramChatManagerBase.from_queryset(TelegramChatQuerySet)


class TelegramGroupMemberQuerySet(models.QuerySet):
    """
    QuerySet for TelegramGroupMemberManager
    """


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
