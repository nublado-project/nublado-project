import logging

from telegram import Update
from telegram.ext import (
    ContextTypes, MessageHandler, filters
)
from telegram.constants import ChatMemberStatus

from django.utils.translation import gettext as _
from django.conf import settings

from django_telegram.functions.chat_actions import send_typing_action
from django_telegram.functions.decorators import (
    restricted_group_member
)
from django_telegram.functions.admin import set_language

from group_notes.bot_commands.group_notes import (
    group_notes as cmd_group_notes,
    save_group_note as cmd_save_group_note,
    remove_group_note as cmd_remove_group_note,
    get_group_note as cmd_get_group_note
)

logger = logging.getLogger('django')

BOT_TOKEN = settings.NUBLADO_BOT_TOKEN
GROUP_ID = settings.NUBLADO_GROUP_ID
REPO_ID = settings.NUBLADO_REPO_ID
OWNER_ID = settings.NUBLADO_GROUP_OWNER_ID
TAG_CHAR = '#'
GET_GROUP_NOTE_REGEX = '^[' + TAG_CHAR + '][a-zA-Z0-9_-]+$'


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
async def group_notes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await set_language(BOT_TOKEN)
    await cmd_group_notes(update, context, group_id=GROUP_ID)


@restricted_group_member(group_id=GROUP_ID, member_status=ChatMemberStatus.OWNER)
@send_typing_action
async def save_group_note(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await set_language(BOT_TOKEN)
    await cmd_save_group_note(update, context, group_id=GROUP_ID, repo_id=REPO_ID)


@restricted_group_member(group_id=GROUP_ID, member_status=ChatMemberStatus.OWNER)
@send_typing_action
async def remove_group_note(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await set_language(BOT_TOKEN)
    await cmd_remove_group_note(update, context, group_id=GROUP_ID)


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
async def get_group_note(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:
    await set_language(BOT_TOKEN)
    await cmd_get_group_note(
        update,
        context,
        group_id=GROUP_ID,
        repo_id=REPO_ID,
        tag_char=TAG_CHAR
    )


get_group_note_handler = MessageHandler(
    filters.Regex(GET_GROUP_NOTE_REGEX),
    get_group_note
)
