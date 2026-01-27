from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import gettext as _

from .utils import _is_group, _is_private


BOT_MESSAGES = {
    "bot_group_only": "bot.message.group_only",
    "bot_private_only": "bot.message.private_only"
}


class HandlerPolicy(ABC):
    @abstractmethod
    async def check(
        self,
        handler,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:
        """
        Return True to allow execution, False to block it.
        Policies may send replies before returning False.
        """
        raise NotImplementedError


class GroupOnly(HandlerPolicy):
    async def check(
        self, 
        handler,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:
        if not _is_group(update.effective_chat):
            tg_message = update.effective_message
            if tg_message:
                bot_message = _(BOT_MESSAGES["bot_group_only"])
                await tg_message.reply_text(
                    bot_message
                )
            return False
        return True


class PrivateOnly(HandlerPolicy):
    async def check(
        self, 
        handler,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:
        if not _is_private(update.effective_chat):
            tg_message = update.effective_message
            if tg_message:
                bot_message = _(BOT_MESSAGES["bot_private_only"])
                await tg_message.reply_text(
                    bot_message
                )
            return False
        return True