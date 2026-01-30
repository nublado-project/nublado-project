from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import activate, get_language, override, gettext as _
from django.conf import settings

from django_telegram.policies import GroupOnly
from django_telegram.utils import set_chat_language, normalize_language_code, safe_reply

from ..bot_messages import BOT_MESSAGES


async def set_bot_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_message = update.effective_message
    tg_chat = update.effective_chat

    # The bot command language-code argument.
    if len(context.args) != 1:
        await tg_message.reply_text(_("Usage: /set_bot_language <language_code>"))
        return

    language_code = normalize_language_code(context.args[0])

    # Check if language_code is in acceptable language codes.
    if not language_code:
        keys = list(settings.LANGUAGES_DICT.keys())
        bot_message = _(BOT_MESSAGES["error_invalid_language_code"]).format(
            language_keys=keys
        )
        await safe_reply(update, bot_message)
        return

    current_language = get_language()
 
    if language_code == current_language:
        bot_message = _(BOT_MESSAGES["bot_language_already_active"]).format(
            language=_(settings.LANGUAGES_DICT[language_code])
        )
        await safe_reply(update, bot_message)
        return

    # If the language_code isn't the current language, update the group settings language and
    # context data bot language, then activate the new language.
    await set_chat_language(update, context, language_code)

    # Temporarily switch the active language ONLY within this block.
    with override(language_code):
        # Build the confirmation message in the newly selected language.
        bot_message = _(BOT_MESSAGES["bot_language_set"]).format(
            language=_(settings.LANGUAGES_DICT[language_code])
        )

    await safe_reply(update, bot_message)


