from django.utils.translation import activate, gettext as _


BOT_MESSAGES = {
    'agree': _("I agree."),
    'welcome': _(
        "Welcome to the group, {name}.\n\n" \
        "Please read the following rules and click the \"I agree\" button to participate.\n\n" \
        "*Rules*\n" \
        "- Communicate in only English and Spanish.\n" \
        "- Be a good example. Help others out with corrections.\n" \
        "- Introduce yourself with a voice message after joining."
    ),
    'welcome_agreed': _(
        "Welcome to the group, {name}.\n\n" \
        "*You need to introduce yourself with a voice message or you will be booted from the group.*\n\n" \
        "This is our our protocol for new members. It helps us filter out fake accounts, trolls, etc.\n\n" \
        "We look forward to hearing from you."
    ),
    'bot_language_set': _("The bot's language has been changed to {language}."),
    'error_invalid_language_key': _("Error: The possible language keys are [{language_keys}].")
}