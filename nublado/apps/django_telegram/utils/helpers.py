from telegram import Update, User, Chat, ChatMember
from telegram.ext import ContextTypes
from telegram.constants import ChatType, ChatMemberStatus

from django.utils.translation import override
from django.conf import settings

from ..constants import CONTEXT_LANGUAGE_KEY


# Helper functions
def _is_group(tg_chat: Chat):
    return tg_chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}


def _is_private(tg_chat: Chat):
    return tg_chat.type == ChatType.PRIVATE


def _is_admin(tg_member: ChatMember):
    return tg_member.status in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ]


def _is_group_owner(tg_member: ChatMember):
    return tg_member.status == ChatMemberStatus.OWNER


def get_username_or_name(user: User):
    """Return user's username or first and last names."""
    if user.username:
        return user.username
    elif user.last_name:
        return f"{user.first_name} {user.last_name}"
    else:
        return user.first_name


def get_context_language(context: ContextTypes.DEFAULT_TYPE):
    return context.chat_data.get(CONTEXT_LANGUAGE_KEY, settings.LANGUAGE_CODE)


def set_context_language(
    context: ContextTypes.DEFAULT_TYPE, language_code: str
):
    context.chat_data[CONTEXT_LANGUAGE_KEY] = language_code


def validate_language_code(language_code: str):
    return language_code in settings.LANGUAGES_DICT


def normalize_language_code(language_code: str):
    language_code = language_code.lower()
    return language_code if validate_language_code(language_code) else None


async def safe_reply(
    update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, **kwargs
):
    """
    Safely reply to a message using the chat's current language.
    Accepts lazy strings.
    """
    message = update.effective_message
    if message:
        language_code = get_context_language(context)
        with override(language_code):
           reply_message = await message.reply_text(str(text).format(**kwargs))
        return reply_message