from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import activate, get_language
from django.conf import settings

from .models import TelegramChat, TelegramGroupSettings

CONTEXT_DATA_BOT_LANGUAGE_KEY = "bot_language"


class BaseTelegramHandler:
    default_language_code = settings.LANGUAGE_CODE
    policies: list = []

    async def get_chat_language(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> str:
        # Try getting the language first from the context data.
        language_code = context.chat_data.get(CONTEXT_DATA_BOT_LANGUAGE_KEY)

        if language_code:
            return language_code
        # If language code not found in context data, get it from the db.
        tg_chat = update.effective_chat
        chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)
        group_settings = (
            await TelegramGroupSettings.objects.filter(chat=chat)
            .only("language")
            .afirst()
        )
        language_code = (
            group_settings.language
            if group_settings and group_settings.language
            else self.default_language_code
        )

        # Store language_code in context data.
        context.chat_data[CONTEXT_DATA_BOT_LANGUAGE_KEY] = language_code
        return language_code

    async def __call__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        language_code = await self.get_chat_language(update, context)
        old_language_code = get_language()

        try:
            # Activate language from language_code.
            activate(language_code)

            # Check policies
            for policy in self.policies:
                allowed = await policy.check(self, update, context)
                if not allowed:
                    return

            return await self.handle(update, context)
        finally:
            activate(old_language_code)

    async def handle(self, update, context):
        """
        Subclasses must implement this.
        """
        raise NotImplementedError
