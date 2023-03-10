import logging

from telegram import Update
from telegram.ext import (
    ContextTypes, MessageHandler, filters
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
from group_points.bot_commands.group_points import (
    add_points as cmd_add_points,
    remove_points as cmd_remove_points
)

logger = logging.getLogger('django')

BOT_TOKEN = settings.NUBLADO_BOT_TOKEN
ADD_POINT_TRIGGER = '\+'
ADD_POINT_REGEX = '^' + ADD_POINT_TRIGGER + '{2}[^' + ADD_POINT_TRIGGER + '][\s\S]*$'
REMOVE_POINT_TRIGGER = '\-'
REMOVE_POINT_REGEX = '^' + REMOVE_POINT_TRIGGER + '{2}[\s\S]*$'
GROUP_ID = settings.NUBLADO_GROUP_ID

# Command handlers 
@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
async def add_points(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await set_language(BOT_TOKEN)
    await cmd_add_points(update, context, GROUP_ID)


@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
async def remove_points(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await set_language(BOT_TOKEN)
    await cmd_remove_points(update, context, GROUP_ID)


# Message handlers to listen for triggers to add or remove points.
add_points_handler = MessageHandler(
    (filters.Regex(ADD_POINT_REGEX) & filters.REPLY),
    add_points
)


remove_points_handler = MessageHandler(
    (filters.Regex(REMOVE_POINT_REGEX) & filters.REPLY),
    remove_points
)
