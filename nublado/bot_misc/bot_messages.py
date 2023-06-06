from django.utils.translation import gettext as _

BOT_MESSAGES = {
    'dice_roll': _("{member} has rolled {dice}."),
    'dice_roll_total': _("{member} has rolled {dice}.\n\n Total: {total}"),
    'dice_specify_num': _("Please specify the number of dice ({min_dice} - {max_dice})."),
    'get_time': _("It's {weekday}, {time} {timezone}."),
    'start_bot': _("Hello, {member}. {bot_name} has started."),
    'hello': _("Hey, {member_receive}.\n{member_send} says hello."),
    'text_required': _("This command requires a text argument."),
    "testing": _("testing testing")
}