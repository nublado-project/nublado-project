import logging

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus

from functools import wraps

from .group import (
    is_group_chat, is_member_status,
    is_group_id
)

logger = logging.getLogger('django')


def restricted_group_id(group_id: int):
    def callable(func):
        @wraps(func)
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
            chat_id = update.effective_chat.id
            bot = context.bot
            if await is_group_id(bot, chat_id, group_id):
                return await func(update, context)
            else:
                return
        return wrapped
    return callable    


# Decorators for command handlers
def restricted_group_chat(func):
    """Restrict access to messages coming from a group chat the bot belongs to."""
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        user = update.effective_user
        if await is_group_chat(context.bot, chat_id):
            return await func(update, context)
        else:
            logger.warning(f"Unauthorized access: {func.__name__} - {user.id} - {user.username}.")
            return
    return wrapped


def restricted_group_member(
        group_id: int,
        member_status: str = ChatMemberStatus.MEMBER,
        group_chat: bool = True,
        private_chat: bool = True
):
    """Restrict access to a group's members determined by member status."""
    def callable(func):
        @wraps(func)
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
            chat_id = update.effective_chat.id
            user = update.effective_user
            bot = context.bot
            if await is_member_status(bot, user.id, group_id, member_status):
                if group_chat and private_chat:
                    # The command can be executed in the group or in a private message with the bot.
                    if await is_group_id(bot, chat_id, group_id) or chat_id == user.id:
                        return await func(update, context)
                    else:
                        return
                elif group_chat:
                    # The command can only be executed in the group chat.
                    if await is_group_id(bot, chat_id, group_id):
                        return await func(update, context)
                    else:
                        return
                elif private_chat:
                    # The command can only be exectued in a private message with the bot.
                    if chat_id == user.id:
                        return await func(update, context)
                    else:
                        return
                else:
                    return
            else:
                return
        return wrapped
    return callable