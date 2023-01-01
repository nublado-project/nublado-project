import logging

from telegram import Update
from telegram.ext import (
    CallbackContext, MessageHandler, Filters
)

from django.conf import settings
from django.utils.translation import gettext as _

from django_telegram.functions.chat_actions import (
    send_typing_action
)
from django_telegram.functions.decorators import (
    restricted_group_member
)
from django_telegram.functions.admin import set_language
from django_telegram.bot_commands import (
    add_points as cmd_add_points,
    remove_points as cmd_remove_points
)

logger = logging.getLogger('django')

BOT_TOKEN = settings.NUBLADO_BOT_TOKEN
ADD_POINTS_TRIGGER = '\+'
ADD_POINTS_REGEX = '^' + ADD_POINTS_TRIGGER + '{2}[\s\S]*$'
REMOVE_POINTS_TRIGGER = '\-'
REMOVE_POINTS_REGEX = '^' + REMOVE_POINTS_TRIGGER + '{2}[\s\S]*$'
GROUP_ID = settings.NUBLADO_GROUP_ID

# Command handlers 
@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
def add_points(update: Update, context: CallbackContext) -> None:
    set_language(BOT_TOKEN)
    cmd_add_points(update, context, GROUP_ID)


@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
def remove_points(update: Update, context: CallbackContext) -> None:
    set_language(BOT_TOKEN)
    cmd_remove_points(update, context, GROUP_ID)


# Message handlers to listen for triggers to add or remove points.
add_points_handler = MessageHandler(
    (Filters.regex(ADD_POINTS_REGEX) & Filters.reply),
    add_points
)


remove_points_handler = MessageHandler(
    (Filters.regex(REMOVE_POINTS_REGEX) & Filters.reply),
    remove_points
)
