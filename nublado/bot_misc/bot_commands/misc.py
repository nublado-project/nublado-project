import random
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _

from django_telegram.functions.functions import (
    parse_command_last_arg_text, compare_strings
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


async def correct_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pending description."""
    if update.message.reply_to_message:
        if update.message.reply_to_message.text:
            reply_to_message_id = update.message.reply_to_message.message_id
            string_a = update.message.reply_to_message.text

            if len(context.args) >= 1:
                string_b = parse_command_last_arg_text(
                    update.effective_message,
                    maxsplit=1
                )
                error_text, correction_text = compare_strings(
                    string_a, string_b
                )

                bot_message = "{} {}\n\n{} {}".format(
                    "⭕️",
                    error_text,
                    "🟢",
                    correction_text
                )
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML,
                    text=bot_message,
                    reply_to_message_id=reply_to_message_id
                )
            else:
                bot_message = _(BOT_MESSAGES['text_required'])
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=bot_message
                )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="This command must be a reply to a text message."
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


async def flip_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = random.randint(0, 1)
    user = update.effective_user

    if result == 0:
        bot_message = _(BOT_MESSAGES['coin_heads']).format(
            member=user.mention_markdown(),
        )
    elif result == 1:
        bot_message = _(BOT_MESSAGES['coin_tails']).format(
            member=user.mention_markdown(),
        )
    else:
        bot_message = "Error: The result needs to return 0 or 1."

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
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


async def alarm(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    await context.bot.send_message(job.chat_id, text=f"Beep! {job.data} seconds are over!")


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()

    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id
    try:
        # args[0] should contain the time for the timer in seconds
        due = float(context.args[0])
        if due < 0:
            await update.effective_message.reply_text("Sorry we can not go back to future!")
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, chat_id=chat_id, name=str(chat_id), data=due)

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        await update.effective_message.reply_text(text)

    except (IndexError, ValueError):
        await update.effective_message.reply_text("Usage: /set <seconds>")


async def unset_timer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)
