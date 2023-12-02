from django.utils.translation import gettext as _

BOT_MESSAGES = {
    'dice_roll': _("bot.message.dice_roll {member} {dice}"),
    'dice_roll_total': _("bot.message.dice_roll_total {member} {dice} {total}"),
    'dice_specify_num': _("bot.message.dice_specify_number {min_dice} {max_dice}"),
    'get_time': _("It's {weekday}, {time} {timezone}."),
    'start_bot': _("Hello, {member}. {bot_name} has started."),
    'hello': _("Hey, {member_receive}.\n{member_send} says hello."),
    'text_required': _("This command requires a text argument."),
    "testing": _("testing testing")
}