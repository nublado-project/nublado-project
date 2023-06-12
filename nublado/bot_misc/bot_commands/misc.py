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
from ..bot_messages import BOT_MESSAGES

logger = logging.getLogger('django')

# Constants for default values.
MIN_DICE = 1
MAX_DICE = 10
MIN_DIE_VAL = 1
MAX_DIE_VAL = 6


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message and prompt a reply on start."""
    user = update.effective_user
    bot_name = context.bot.first_name
    bot_message = _(BOT_MESSAGES['start_bot']).format(
        member=user.mention_markdown(),
        bot_name=bot_name
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot_message
    )


async def test_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a dummy message for testing."""
    bot_message = _(BOT_MESSAGES['testing'])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot_message
    )


async def get_time_utc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the current date/time in UTC format."""
    weekday = timezone.now().weekday()
    bot_message = _(BOT_MESSAGES['get_time']).format(
        weekday=_(settings.WEEKDAYS[weekday]),
        time=timezone.now().strftime('%H:%M'),
        timezone=settings.TIME_ZONE
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot_message
    )


async def reverse_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reverse the text provided as an argument and display it."""
    if len(context.args) >= 1:
        bot_message = parse_command_last_arg_text(
            update.effective_message,
            maxsplit=1
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=bot_message[::-1]
        )
    else:
        bot_message = _(BOT_MESSAGES['text_required'])
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=bot_message
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
                bot_message = _(BOT_MESSAGES['hello']).format(
                    member_receive=chat_member.user.mention_markdown(),
                    member_send=user.mention_markdown()
                )
                await context.bot.send_message(
                    chat_id=group_id,
                    text=bot_message
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
            bot_message = parse_command_last_arg_text(
                update.effective_message,
                maxsplit=1
            )
            await context.bot.send_message(
                chat_id=group_id,
                text=bot_message
            )


async def roll_dice_c(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    min_dice=MIN_DICE,
    max_dice=MAX_DICE,
    dice_min_val=MIN_DIE_VAL,
    dice_max_val=MAX_DIE_VAL,
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
                bot_message = _(BOT_MESSAGES['dice_roll_total']).format(
                    member=user.mention_markdown(),
                    dice=results,
                    total=total
                )
            else:
                bot_message = _(BOT_MESSAGES['dice_roll']).format(
                    member=user.mention_markdown(),
                    dice=results
                )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=bot_message 
            )
        else:
            bot_message = _(BOT_MESSAGES['dice_specify_num']).format(
                min_dice=min_dice,
                max_dice=max_dice
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=bot_message
            )
    else:
        bot_message = _(BOT_MESSAGES['dice_specify_num']).format(
            min_dice=min_dice,
            max_dice=max_dice
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=bot_message
        )

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll specified number of dice and show results as text."""
    await roll_dice_c(update, context, dice_sum=False)


async def roll_sum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll specified number of dice and show results as text."""
    await roll_dice_c(update, context, dice_sum=True)
