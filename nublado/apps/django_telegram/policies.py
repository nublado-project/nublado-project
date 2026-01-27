from abc import ABC, abstractmethod
from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop

from django.utils.translation import activate, get_language, gettext as _
from django.conf import settings

from .utils import _is_group, _is_private


BOT_MESSAGES = {
    "bot_group_only": "bot.message.group_only",
    "bot_private_only": "bot.message.private_only"
}


def with_policies(*policies):
    def decorator(callback):
        @wraps(callback)
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
            language_resolver = context.application.bot_data.get("language_resolver")
            old_language = get_language() or settings.LANGUAGE_CODE

            try:
                if language_resolver:
                    language_code = await language_resolver(update, context)
                    activate(language_code)

                for policy in policies:
                    allowed = await policy.check(update, context)
                    if not allowed:
                        raise ApplicationHandlerStop

                return await callback(update, context)

            finally:
                activate(old_language)

        return wrapped
    return decorator


class HandlerPolicy(ABC):
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
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:
        tg_chat = update.effective_chat
        if not tg_chat or not _is_private(tg_chat):
            tg_message = update.effective_message
            if tg_message:
                bot_message = _(BOT_MESSAGES["bot_private_only"])
                await tg_message.reply_text(
                    bot_message
                )
            return False
        return True