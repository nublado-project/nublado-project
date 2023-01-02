import logging

from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import CHATMEMBER_CREATOR

from django.conf import settings
from django.utils.translation import gettext as _

from django_telegram.functions.chat_actions import send_typing_action
from django_telegram.functions.decorators import restricted_group_member
from bot_misc.bot_commands.misc import (
    start as cmd_start,
    get_time as cmd_get_time,
    reverse_text as cmd_reverse_text,
    echo as cmd_echo,
    hello as cmd_hello,
    roll as cmd_roll,
    roll_sum as cmd_roll_sum
)

logger = logging.getLogger('django')

# To do:Verify that  bot is in group.
GROUP_ID = settings.NUBLADO_GROUP_ID


@restricted_group_member(group_id=GROUP_ID, group_chat=False)
@send_typing_action
def start(update: Update, context: CallbackContext) -> None:
    """Send a message and prompt a reply on start."""
    cmd_start(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
def hello(update: Update, context: CallbackContext) -> None:
    cmd_hello(update, context, GROUP_ID)


@restricted_group_member(group_id=GROUP_ID, member_status=CHATMEMBER_CREATOR)
@send_typing_action
def echo(update: Update, context: CallbackContext) -> None:
    """Echo a message to the group."""
    cmd_echo(update, context, GROUP_ID)


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
def get_time(update: Update, context: CallbackContext) -> None:
    """Display the current time."""
    cmd_get_time(update, context)


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
def reverse_text(update: Update, context: CallbackContext) -> None:
    """Reverse the text provided as an argument and display it."""
    cmd_reverse_text(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=True)
@send_typing_action
def roll(update: Update, context: CallbackContext) -> None:
    """Roll specified number of dice and show results as text."""
    cmd_roll(update, context)


@restricted_group_member(group_id=GROUP_ID, private_chat=True)
@send_typing_action
def roll_sum(update: Update, context: CallbackContext) -> None:
    """Roll specified number of dice and show results as text."""
    cmd_roll_sum(update, context)