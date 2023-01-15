import random
import logging

from telegram import Update
from telegram.ext import ContextTypes

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _

from django_telegram.functions.functions import (
    parse_command_last_arg_text
)
from django_telegram.functions.group import (
    get_random_group_member
)

logger = logging.getLogger('django')

BOT_MESSAGES = {
    'dice_roll': _("{member} has rolled {dice}."),
    'dice_roll_total': _("{member} has rolled {dice}.\n\n Total: {total}"),
    'dice_specify_num': _("Please specify the number of dice ({min_dice} - {max_dice})."),
    'get_time': _("It's {weekday}, {time} {timezone}."),
    'start_bot': _("Hello, {member}. {bot_name} has started."),
    'hello': _("Hey, {member_receive}.\n{member_send} says hello.")
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message and prompt a reply on start."""
    user = update.effective_user
    bot_name = context.bot.first_name
    message = _(BOT_MESSAGES['start_bot']).format(
        member=user.mention_markdown(),
        bot_name=bot_name
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the current time."""
    weekday = timezone.now().weekday()
    message = _(BOT_MESSAGES['get_time']).format(
        weekday=_(settings.WEEKDAYS[weekday]),
        time=timezone.now().strftime('%H:%M'),
        timezone=settings.TIME_ZONE
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


async def reverse_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reverse the text provided as an argument and display it."""
    if len(context.args) >= 1:
        message = parse_command_last_arg_text(
            update.effective_message,
            maxsplit=1
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message[::-1]
        )
    else:
        message = _("The command requires some text to be reversed.")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )


async def hello(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None
) -> None:
    if group_id:
        member = await get_random_group_member(group_id)
        if member:
            try:
                user = update.effective_user
                chat_member = await context.bot.get_chat_member(group_id, member.user_id)
                message = _(BOT_MESSAGES['hello']).format(
                    member_receive=chat_member.user.mention_markdown(),
                    member_send=user.mention_markdown()
                )
                await context.bot.send_message(
                    chat_id=group_id,
                    text=message
                )
            except:
                pass


async def echo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None
) -> None:
    """Echo a message to the group."""
    if group_id:
        if len(context.args) >= 1:
            message = parse_command_last_arg_text(
                update.effective_message,
                maxsplit=1
            )
            await context.bot.send_message(
                chat_id=group_id,
                text=message
            )


async def roll_dice_c(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    min_dice=1,
    max_dice=10,
    dice_min_val=1,
    dice_max_val=6,
    dice_sum=False
):
    if len(context.args) >= 1:
        int_arg = int(context.args[0])
        if int_arg >= min_dice and int_arg <= max_dice:
            num_dice = int_arg
            results = []
            user = update.effective_user
            for x in range(num_dice):
                result = random.randint(dice_min_val, dice_max_val)
                results.append(result)
            if dice_sum:
                total = sum(results)
                message = _(BOT_MESSAGES['dice_roll_total']).format(
                    member=user.mention_markdown(),
                    dice=results,
                    total=total
                )
            else:
                message = _(BOT_MESSAGES['dice_roll']).format(
                    member=user.mention_markdown(),
                    dice=results
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message 
            )
    else:
        message = _(BOT_MESSAGES['dice_specify_num']).format(
            min_dice=min_dice,
            max_dice=max_dice
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll specified number of dice and show results as text."""
    await roll_dice_c(update, context, dice_sum=False)


async def roll_sum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll specified number of dice and show results as text."""
    await roll_dice_c(update, context, dice_sum=True)
