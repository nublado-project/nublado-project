from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import activate, get_language

from .models import TelegramChat, TelegramGroupSettings


def chat_language(handler_func):
    @wraps(handler_func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        # Try getting the language first from the context data. 
        language = context.chat_data.get("bot_language")

        if not language:
            # If language not found in context data, get it from the db. 
            tg_chat = update.effective_chat
            chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)
            group_settings = (
                await TelegramGroupSettings.objects
                .filter(chat=chat)
                .only("language")
                .afirst()
            )
            language = (
                group_settings.language
                if group_settings and group_settings.language
                else "en"
            )

            # Store language in context chat data.
            context.chat_data["bot_language"] = language

        # Activate language.
        old_language = get_language()
        try:
            activate(language)
            return await handler_func(update, context, *args, **kwargs)
        finally:
            activate(old_language)

    return wrapper