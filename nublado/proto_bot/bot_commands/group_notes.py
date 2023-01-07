import logging

from telegram import Update
from telegram.ext import (
    CallbackContext, MessageHandler, Filters
)
from telegram.constants import CHATMEMBER_ADMINISTRATOR

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

BOT_TOKEN = settings.PROTO_BOT_TOKEN
GROUP_ID = settings.PROTO_GROUP_ID
REPO_ID = settings.PROTO_REPO_ID
OWNER_ID = settings.PROTO_GROUP_OWNER_ID
TAG_CHAR = '#'
GET_GROUP_NOTE_REGEX = '^[' + TAG_CHAR + '][a-zA-Z0-9_-]+$'


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
def group_notes(update: Update, context: CallbackContext) -> None:
    set_language(BOT_TOKEN)
    cmd_group_notes(update, context, group_id=GROUP_ID)


@restricted_group_member(group_id=GROUP_ID, member_status=CHATMEMBER_ADMINISTRATOR)
@send_typing_action
def save_group_note(update: Update, context: CallbackContext) -> None:
    set_language(BOT_TOKEN)
    cmd_save_group_note(update, context, group_id=GROUP_ID, repo_id=REPO_ID)


@restricted_group_member(group_id=GROUP_ID, member_status=CHATMEMBER_ADMINISTRATOR)
@send_typing_action
def remove_group_note(update: Update, context: CallbackContext) -> None:
    set_language(BOT_TOKEN)
    cmd_remove_group_note(update, context, group_id=GROUP_ID)


@restricted_group_member(group_id=GROUP_ID)
@send_typing_action
def get_group_note(update: Update, context: CallbackContext) -> None:
    set_language(BOT_TOKEN)
    cmd_get_group_note(
        update,
        context,
        group_id=GROUP_ID,
        repo_id=REPO_ID,
        tag_char=TAG_CHAR
    )


get_group_note_handler = MessageHandler(
    Filters.regex(GET_GROUP_NOTE_REGEX),
    get_group_note
)
