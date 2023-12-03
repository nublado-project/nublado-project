from django.utils.translation import gettext_lazy as _


BOT_MESSAGES = {
    'no_give_bot': _("bot.message.no_give_points_bot {points_name}"),
    'no_take_bot': _("You can't take {points_name} from a bot."),
    'no_give_self': _("You can't give {points_name} to yourself."),
    'no_take_self': _("You can't take {points_name} from yourself."),
    'give_point': _(
        "*{sender_name} ({member_sender})* has given a " + \
        "{points_name} to *{receiver_name} ({receiver_points})*."
    ),
    'give_points': _(
        "*{sender_name} ({member_sender})* has given {num_points} " + \
        "{points_name} to *{receiver_name} ({receiver_points})*."
    ),
    'take_point': _(
        "*{sender_name} ({member_sender})* has taken a " + \
        "{points_name} from *{receiver_name} ({receiver_points})*."
    ),
    'take_points': _(
        "*{sender_name} ({member_sender})* has taken {num_points} " + \
        "{points_name} from *{receiver_name} ({receiver_points})*."
    ),
}
