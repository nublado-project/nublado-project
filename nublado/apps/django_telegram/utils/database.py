from telegram import Update
from telegram.ext import ContextTypes

from ..models import TelegramChat, TelegramGroupSettings
from ..constants import CONTEXT_LANGUAGE_KEY
from .helpers import get_context_language, set_context_language


"""
Helpers that can touch the database. I put them here to avoid AppRegristry errors.
"""


async def resolve_chat_language(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:

    if CONTEXT_LANGUAGE_KEY in context.chat_data:
        return get_context_language(context)

    tg_chat = update.effective_chat
    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)

    group_settings = (
        await TelegramGroupSettings.objects.filter(chat=chat).only("language").afirst()
    )

    language_code = (
        group_settings.language
        if group_settings and group_settings.language
        else settings.LANGUAGE_CODE
    )

    set_context_language(context, language_code)

    return language_code


async def set_chat_language(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    language_code: str,
) -> None:
    tg_chat = update.effective_chat

    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)
    group_settings, created = await TelegramGroupSettings.objects.aget_or_create(
        chat=chat
    )
    group_settings.language = language_code
    await group_settings.asave()

    # Set context data to store language_code
    set_context_language(context, language_code)


