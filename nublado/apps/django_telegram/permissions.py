from functools import wraps

from telegram.constants import ChatType, ChatMemberStatus


# Helper functions
def _is_group(chat):
    return chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}


def _is_private(chat):
    return chat.type == ChatType.PRIVATE


# Permission decorators
def group_only(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        if not _is_group(update.effective_chat):
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


def private_only(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        if not _is_private(update.effective_chat):
            return
        return await func(update, context, *args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        chat = update.effective_chat
        user = update.effective_user

        if not _is_group(chat):
            return

        member = await chat.get_member(user.id)
        if member.status not in {
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        }:
            await update.effective_message.reply_text("Admins only.")
            return

        return await func(update, context, *args, **kwargs)
    return wrapper


def owner_required(func):
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        chat = update.effective_chat
        user = update.effective_user

        if not _is_group(chat):
            return

        member = await chat.get_member(user.id)
        if member.status != ChatMemberStatus.OWNER:
            await update.effective_message.reply_text("Group owner only.")
            return

        return await func(update, context, *args, **kwargs)
    return wrapper