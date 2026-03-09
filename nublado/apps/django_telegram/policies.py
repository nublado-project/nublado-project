from abc import ABC, abstractmethod
from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop

from django.utils.translation import gettext as _

from .utils.helpers import _is_group, _is_private, _is_admin, _is_group_owner, safe_reply

BOT_MESSAGES = {
    "bot_group_only": "bot.message.group_only",
    "bot_private_only": "bot.message.private_only",
}


class HandlerPolicy(ABC):
    async def _reply(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str
    ):
        await safe_reply(update, context, message)

    async def _reply_and_block(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str
    ) -> bool:
        await self._reply(update, context, message)
        return False

    @abstractmethod
    async def check(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:
        """
        Return True to allow execution, False to block it.
        Policies may send replies before returning False.
        """
        ...


class GroupOnly(HandlerPolicy):
    async def check(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:
        tg_chat = update.effective_chat
        if not tg_chat or not _is_group(tg_chat):
            return await self._reply_and_block(
                update, context, _(BOT_MESSAGES["bot_group_only"])
            )
        return True


class PrivateOnly(HandlerPolicy):
    async def check(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:
        tg_chat = update.effective_chat
        if not tg_chat or not _is_private(tg_chat):
            return await self._reply_and_block(
                update, context, _(BOT_MESSAGES["bot_private_only"])
            )
        return True


class AdminOnly(HandlerPolicy):
    async def check(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:

        tg_chat = update.effective_chat
        tg_user = update.effective_user

        if not tg_chat or not tg_user:
            return False

        try:
            tg_member = await context.bot.get_chat_member(tg_chat.id, tg_user.id)
        except Exception:
            return await self._reply_and_block(
                update, context, "Could not verify admin status."
            )

        if not _is_admin(tg_member):
            return await self._reply_and_block(
                update,
                context,
                "This command is restricted to admins.",
            )

        return True


class GroupOwnerOnly(HandlerPolicy):
    async def check(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:

        tg_chat = update.effective_chat
        tg_user = update.effective_user

        if not tg_chat or not tg_user:
            return False

        try:
            tg_member = await context.bot.get_chat_member(tg_chat.id, tg_user.id)
        except Exception:
            return await self._reply_and_block(
                update, context, "Could not verify owner status."
            )

        if not _is_group_owner(tg_member):
            return await self._reply_and_block(
                update,
                context,
                "This command is restricted to the group owner.",
            )

        return True


def with_policies(*policy_classes):
    def decorator(callback):

        policies = [p() for p in policy_classes]

        @wraps(callback)
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):

            for policy in policies:
                allowed = await policy.check(update, context)
                if not allowed:
                    raise ApplicationHandlerStop

            return await callback(update, context)

        return wrapped

    return decorator
