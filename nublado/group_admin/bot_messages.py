from django.utils.translation import activate, gettext_lazy as _


BOT_MESSAGES = {
    'agree': _("bot.message.i_agree"),
    'welcome': _("bot.message.welcome {name}"),
    'welcome_agreed': _("bot.message.welcome_agreed {name}"),
    'bot_language_set': _("bot.message.language_set {language}"),
    'error_invalid_language_key': _("bot.message.invalid_language_key {language_keys}")
}