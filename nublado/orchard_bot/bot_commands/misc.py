import logging

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus

from django.conf import settings
from django.utils.translation import gettext as _

from django_telegram.functions.chat_actions import send_typing_action
from django_telegram.functions.decorators import restricted_group_member
from django_telegram.functions.admin import set_language
from bot_misc.bot_commands.misc import (
    start as cmd_start,
    get_time_utc as cmd_get_time_utc,
    reverse_text as cmd_reverse_text,
    echo as cmd_echo,
    hello as cmd_hello,
    flip_coin as cmd_flip_coin,
    roll as cmd_roll,
    roll_sum as cmd_roll_sum,
    correct_text as cmd_correct_text
)

logger = logging.getLogger('django')

BOT_ID = settings.ORCHARD_BOT
GROUP_ID = settings.ORCHARD_GROUP_ID


@restricted_group_member(group_id=GROUP_ID, group_chat=False)
@send_typing_action
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message and prompt a reply on start."""
    await set_language(BOT_ID)
    await cmd_start(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_language(BOT_ID)
    await cmd_hello(update, context, GROUP_ID)


@restricted_group_member(group_id=GROUP_ID, private_chat=True)
@send_typing_action
async def flip_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Flip a coin and display the result as text."""
    await set_language(BOT_ID)
    await cmd_flip_coin(update, context)


@restricted_group_member(group_id=GROUP_ID, member_status=ChatMemberStatus.OWNER)
@send_typing_action
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo a message to the group."""
    await set_language(BOT_ID)
    await cmd_echo(update, context, GROUP_ID)


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
async def get_time_utc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the current date/time in UTC format."""
    await set_language(BOT_ID)
    await cmd_get_time_utc(update, context)


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
async def reverse_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reverse the text provided as an argument and display it."""
    await set_language(BOT_ID)
    await cmd_reverse_text(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=True)
@send_typing_action
async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll specified number of dice and show results as text."""
    await set_language(BOT_ID)
    await cmd_roll(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=True)
@send_typing_action
async def roll_sum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll specified number of dice and show results as text."""
    await set_language(BOT_ID)
    await cmd_roll_sum(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
async def correct_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_language(BOT_ID)
    await cmd_correct_text(update, context)