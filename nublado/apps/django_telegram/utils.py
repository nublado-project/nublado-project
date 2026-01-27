from telegram import Update, User
from telegram.ext import ContextTypes
from telegram.constants import ChatType, ChatMemberStatus

from django.conf import settings

from .models import TelegramChat, TelegramGroupSettings

LANGUAGE_KEY = "bot_language"

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


def validate_language_code(language_code: str) -> bool:
    return language_code in settings.LANGUAGES_DICT


def normalize_language_code(language_code: str) -> str | None:
    language_code = language_code.lower()
    return language_code if validate_language_code(language_code) else None


async def resolve_chat_language(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> str:

    if LANGUAGE_KEY in context.chat_data:
        return context.chat_data[LANGUAGE_KEY]

    tg_chat = update.effective_chat
    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)

    group_settings = await TelegramGroupSettings.objects.filter(
        chat=chat
    ).only("language").afirst()

    language_code = (
        group_settings.language
        if group_settings and group_settings.language
        else settings.LANGUAGE_CODE
    )

    context.chat_data[LANGUAGE_KEY] = language_code
    return language_code


async def set_chat_language(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    language_code: str,
) -> None:
    tg_chat = update.effective_chat

    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)
    group_settings, created = await TelegramGroupSettings.objects.aget_or_create(chat=chat)
    group_settings.language = language_code
    await group_settings.asave()

    # Set context data to store language_code
    context.chat_data[LANGUAGE_KEY] = language_code


async def safe_reply(update: Update, text: str):
    """
    Safely reply to a message if it exists.
    """

    message = update.effective_message
    if message:
        await message.reply_text(text)