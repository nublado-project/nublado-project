from telegram import Update, User
from telegram.ext import ContextTypes

from django.utils.translation import activate, get_language, gettext_lazy as _
from django.conf import settings

from django_telegram.permissions import group_only
from django_telegram.handlers import BaseTelegramHandler
from django_telegram.models import TelegramChat, TelegramGroupSettings

BOT_MESSAGES = {
    # 'agree': _("bot.message.i_agree"),
    # 'welcome': _("bot.message.welcome {name}"),
    # 'welcome_agreed': _("bot.message.welcome_agreed {name}"),
    "bot_language_set": _("bot.message.language_set {language}"),
    "bot_language_already_active": _("bot.message.language_already_active {language}"),
    "error_invalid_language_code": _(
        "bot.message.invalid_language_key: {language_keys}"
    ),
}

CONTEXT_DATA_BOT_LANGUAGE_KEY = "bot_language"


class SetBotLanguageHandler(BaseTelegramHandler):
    @group_only
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        tg_message = update.effective_message
        tg_chat = update.effective_chat

        # The bot command language-code argument.
        if len(context.args) != 1:
            await tg_message.reply_text(_("Usage: /set_bot_language <language_code>"))
            return
        language_code = context.args[0].lower()

        # Check if language_code is in acceptable language codes.
        if language_code not in settings.LANGUAGES_DICT:
            keys = list(settings.LANGUAGES_DICT.keys())
            bot_message = _(BOT_MESSAGES["error_invalid_language_code"]).format(
                language_keys=keys
            )
            await tg_message.reply_text(bot_message)
            return

        current_language = get_language()
        # If the language_code isn't the current language, update the group settings language and
        # context data bot language, then activate the new language.
        if language_code != current_language:
            chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)
            group_settings, group_settings_created = (
                await TelegramGroupSettings.objects.aget_or_create(chat=chat)
            )
            group_settings.language = language_code
            await group_settings.asave()

            context.chat_data[CONTEXT_DATA_BOT_LANGUAGE_KEY] = language_code
            activate(language_code)

            bot_message = BOT_MESSAGES["bot_language_set"].format(
                language=_(settings.LANGUAGES_DICT[language_code])
            )
            await tg_message.reply_text(bot_message)
        else:
            bot_message = BOT_MESSAGES["bot_language_already_active"].format(
                language=_(settings.LANGUAGES_DICT[language_code])
            )
            await tg_message.reply_text(bot_message)
