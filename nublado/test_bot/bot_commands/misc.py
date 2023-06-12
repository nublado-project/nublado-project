import logging

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatMemberStatus

from django.conf import settings
from django.utils.translation import gettext as _

from django_telegram.functions.chat_actions import send_typing_action
from django_telegram.functions.decorators import restricted_group_member
from bot_misc.bot_commands.misc import (
    start as cmd_start,
    test_bot as cmd_test_bot,
    get_time_utc as cmd_get_time_utc,
    reverse_text as cmd_reverse_text,
    echo as cmd_echo,
    hello as cmd_hello,
    roll as cmd_roll,
    roll_sum as cmd_roll_sum
)

logger = logging.getLogger('django')

# To do:Verify that  bot is in group.
GROUP_ID = settings.TEST_GROUP_ID


@restricted_group_member(group_id=GROUP_ID, group_chat=False)
@send_typing_action
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message and prompt a reply on start."""
    await cmd_start(update, context)


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
async def test_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test the bot's resonsiveness by posting a dummy message."""
    await cmd_test_bot(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_hello(update, context, GROUP_ID)


@restricted_group_member(group_id=GROUP_ID, member_status=ChatMemberStatus.OWNER)
@send_typing_action
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo a message to the group."""
    await cmd_echo(update, context, GROUP_ID)


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
async def get_time_utc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display the current date/time in UTC format."""
    await cmd_get_time_utc(update, context)


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
async def reverse_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reverse the text provided as an argument and display it."""
    await cmd_reverse_text(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=True)
@send_typing_action
async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll specified number of dice and show results as text."""
    await cmd_roll(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=True)
@send_typing_action
async def roll_sum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll specified number of dice and show results as text."""
    await cmd_roll_sum(update, context)