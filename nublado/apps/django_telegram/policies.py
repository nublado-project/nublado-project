from abc import ABC, abstractmethod
from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop

from django.utils.translation import activate, get_language, gettext as _
from django.conf import settings

from .utils import _is_group, _is_private, safe_reply


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
                # Activate language.
                if language_resolver:
                    language_code = await language_resolver(update, context)
                    activate(language_code)

                # Check policies.
                for policy in policies:
                    allowed = await policy.check(update, context)
                    if not allowed:
                        raise ApplicationHandlerStop

                # Call original handler.
                return await callback(update, context)

            finally:
                activate(old_language)

        return wrapped
    return decorator


class HandlerPolicy(ABC):
    async def reply(self, update: Update, message: str):
        await safe_reply(update, message)

    async def reply_and_block(self, update: Update, message: str) -> bool:
        await self.reply(update, message)
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
            return await self.reply_and_block(update, _(BOT_MESSAGES["bot_group_only"]))
        return True


class PrivateOnly(HandlerPolicy):
    async def check(
        self, 
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> bool:
        tg_chat = update.effective_chat
        if not tg_chat or not _is_private(tg_chat):
            return await self.reply_and_block(update, _(BOT_MESSAGES["bot_private_only"]))
        return True


# To do: Convert these into policies.
# def admin_required(func):
#     @wraps(func)
#     async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         chat = update.effective_chat
#         user = update.effective_user

#         if not _is_group(chat):
#             return

#         member = await chat.get_member(user.id)
#         if member.status not in {
#             ChatMemberStatus.ADMINISTRATOR,
#             ChatMemberStatus.OWNER,
#         }:
#             await update.effective_message.reply_text(
#                 _("This command is for admins only.")
#             )
#             return

#         return await func(self, update, context)

#     return wrapper


# def owner_required(func):
#     @wraps(func)
#     async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
#         chat = update.effective_chat
#         user = update.effective_user

#         if not _is_group(chat):
#             return

#         member = await chat.get_member(user.id)
#         if member.status != ChatMemberStatus.OWNER:
#             await update.effective_message.reply_text(
#                 _("This command is for the group owner only.")
#             )
#             return

#         return await func(self, update, context)

#     return wrapper