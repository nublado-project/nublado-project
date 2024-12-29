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

BOT_ID = settings.ORCHARD_BOT
ADD_POINT_TRIGGER = '\+'
ADD_POINT_REGEX = '^' + ADD_POINT_TRIGGER + '{2}(?!' + ADD_POINT_TRIGGER + ')[\s\S]*$'
ADD_POINTS_REGEX = '^' + ADD_POINT_TRIGGER + '{3}(?!' + ADD_POINT_TRIGGER + ')[\s\S]*$'

REMOVE_POINT_TRIGGER = '\-'
REMOVE_POINT_REGEX = '^' + REMOVE_POINT_TRIGGER + '{2}(?!' + REMOVE_POINT_TRIGGER + ')[\s\S]*$'
REMOVE_POINTS_REGEX = '^' + REMOVE_POINT_TRIGGER + '{3}(?!' + REMOVE_POINT_TRIGGER + ')[\s\S]*$'

GROUP_ID = settings.ORCHARD_GROUP_ID
POINT_NAME = "bot.orchard.point_name"
POINTS_NAME="bot.orchard.points_name"

# Command handlers 
@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
async def add_point(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await set_language(BOT_ID)
    await cmd_add_points(
        update,
        context,
        group_id=GROUP_ID,
        point_name=POINT_NAME
    )

@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
async def add_points(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await set_language(BOT_ID)
    await cmd_add_points(
        update,
        context,
        num_points=2,
        group_id=GROUP_ID,
        points_name=POINTS_NAME
    )

@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
async def remove_point(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await set_language(BOT_ID)
    await cmd_remove_points(
        update,
        context,
        num_points=1,
        group_id=GROUP_ID,
        point_name=POINT_NAME
    )


@restricted_group_member(group_id=GROUP_ID, private_chat=False)
@send_typing_action
async def remove_points(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await set_language(BOT_ID)
    await cmd_remove_points(
        update,
        context,
        num_points=2,
        group_id=GROUP_ID,
        points_name=POINTS_NAME
    )


# Message handlers to listen for triggers to add or remove points.
add_point_handler = MessageHandler(
    (filters.Regex(ADD_POINT_REGEX) & filters.REPLY),
    add_point
)

add_points_handler = MessageHandler(
    (filters.Regex(ADD_POINTS_REGEX) & filters.REPLY),
    add_points
)

remove_point_handler = MessageHandler(
    (filters.Regex(REMOVE_POINT_REGEX) & filters.REPLY),
    remove_point
)

remove_points_handler = MessageHandler(
    (filters.Regex(REMOVE_POINTS_REGEX) & filters.REPLY),
    remove_points
)
