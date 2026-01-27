from django.utils.translation import gettext_lazy as _

BOT_MESSAGES = {
    "bot_start": _("bot.message.start"),
    "bot_hello": _("bot.message.hello"),

    'agree': _("bot.message.i_agree"),
    'welcome': _("bot.message.welcome {name}"),
    'welcome_agreed': _("bot.message.welcome_agreed {name}"),
    "bot_language_set": _("bot.message.language_set {language}"),
    "bot_language_already_active": _("bot.message.language_already_active {language}"),
    "error_invalid_language_code": _("bot.message.invalid_language_key: {language_keys}"),

    "no_give_bot": _("bot.message.no_give_points_bot {points_name}"),
    "no_take_bot": _("bot.message.no_take_points_bot {points_name}"),
    "no_give_self": _("bot.message.no_give_points_self {points_name}"),
    "no_take_self": _("bot.message.no_take_points_self {points_name}"),
    "give_point":
        _("bot.message.give_point_member {sender_name} {sender_points} "
        + "{points_name} {receiver_name} {receiver_points}")
    ,
    "give_points":
        _("bot.message.give_points_member {sender_name} {sender_points} {num_points} "
        + "{points_name} {receiver_name} {receiver_points}")
    ,
    "take_point": _(
        "bot.message.take_point_member {sender_name} {sender_points} " + \
        "{points_name} {receiver_name} {receiver_points}"
    ),
    "take_points": _(
        "bot.message.take_points_member {sender_name} {sender_points} {num_points} " + \
        "{points_name} {receiver_name} {receiver_points}"
    ),  
}