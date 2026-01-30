from telegram import Update, User
from telegram.ext import ContextTypes
from telegram.constants import ChatType

from django.utils.translation import override
from django.conf import settings

from ..constants import CONTEXT_LANGUAGE_KEY


# Helper functions
def _is_group(tg_chat):
    return tg_chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}


def _is_private(tg_chat):
    return tg_chat.type == ChatType.PRIVATE


def get_username_or_name(user: User) -> str:
    """Return user's username or first and last names."""
    if user.username:
        return user.username
    elif user.last_name:
        return f"{user.first_name} {user.last_name}"
    else:
        return user.first_name


def get_context_language(context: ContextTypes.DEFAULT_TYPE) -> str:
    return context.chat_data.get(CONTEXT_LANGUAGE_KEY, settings.LANGUAGE_CODE)


def set_context_language(context: ContextTypes.DEFAULT_TYPE, language_code: str) -> None:
    context.chat_data[CONTEXT_LANGUAGE_KEY] = language_code


def validate_language_code(language_code: str) -> bool:
    return language_code in settings.LANGUAGES_DICT


def normalize_language_code(language_code: str) -> str | None:
    language_code = language_code.lower()
    return language_code if validate_language_code(language_code) else None


async def safe_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, **kwargs):
    """
    Safely reply to a message using the chat's current language.
    Accepts lazy strings.
    """

    message = update.effective_message
    if message:
        language_code = get_context_language(context)
        with override(language_code):
            await message.reply_text(str(text).format(**kwargs))
