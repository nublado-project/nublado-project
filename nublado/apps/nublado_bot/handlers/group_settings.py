from telegram import Update, User
from telegram.ext import ContextTypes

from django.utils.translation import activate, gettext as _
from django.conf import settings

from django_telegram.permissions import group_only
from django_telegram.models import TelegramChat, TelegramGroupSettings

@group_only
async def set_bot_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    chat = update.effective_chat

    if len(context.args) != 1:
        await message.reply_text(_("Usage: /set_bot_language <language_code>"))
        return

    language_code = context.args[0].lower()

    if language_code not in settings.LANGUAGES_DICT:
        await message.reply_text("Invalid language code")
        return


    tg_chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(chat)
    tg_group_settings, tg_group_settings_created = await TelegramGroupSettings.objects.aget_or_create(chat=tg_chat)

    settings.bot_language = language_code
    await tg_group_settings.asave()

    activate(language_code)

    await message.reply_text(
        _("Bot language has changed")
    )