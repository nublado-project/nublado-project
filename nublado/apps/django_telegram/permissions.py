from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import gettext as _

from .utils import _is_group, _is_private


# Decorators
# Note: These are meant to be used with BaseTelegramHandler to decorate the handle method,
# hence the "self" in the method signatures.
def group_only(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not _is_group(update.effective_chat):
            await update.effective_message.reply_text(
                _("This command can only be used in groups.")
            )
            return
        return await func(self, update, context)

    return wrapper


def private_only(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not _is_private(update.effective_chat):
            await update.effective_message.reply_text(
                _("This command can only be used in a private chat.")
            )
            return
        return await func(self, update, context)

    return wrapper


def admin_required(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        user = update.effective_user

        if not _is_group(chat):
            return

        member = await chat.get_member(user.id)
        if member.status not in {
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        }:
            await update.effective_message.reply_text(
                _("This command is for admins only.")
            )
            return

        return await func(self, update, context)

    return wrapper


def owner_required(func):
    @wraps(func)
    async def wrapper(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.effective_chat
        user = update.effective_user

        if not _is_group(chat):
            return

        member = await chat.get_member(user.id)
        if member.status != ChatMemberStatus.OWNER:
            await update.effective_message.reply_text(
                _("This command is for the group owner only.")
            )
            return

        return await func(self, update, context)

    return wrapper
