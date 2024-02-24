from django.utils.translation import gettext_lazy as _

BOT_MESSAGES = {
    'coin_heads': _("bot.message.coin_heads {member}"),
    'coin_tails': _("bot.message.coin_tails {member}"),
    'dice_roll': _("bot.message.dice_roll {member} {dice}"),
    'dice_roll_total': _("bot.message.dice_roll_total {member} {dice} {total}"),
    'dice_specify_num': _("bot.message.dice_specify_number {min_dice} {max_dice}"),
    'get_time': _("It's {weekday}, {time} {timezone}."),
    'start_bot': _("bot.message.bot_start {member} {bot_name}"),
    'hello': _("bot.message.hello {member_receive} {member_send}"),
    'text_required': _("bot.message.text_required"),
    "testing": _("bot.message.testing")
}