import logging

from telegram import Update
from telegram.ext import (
    CallbackContext, CallbackQueryHandler,
    MessageHandler, Filters
)
from telegram.constants import CHATMEMBER_ADMINISTRATOR

from django.conf import settings


from django_telegram.functions.admin import set_language
from django_telegram.functions.chat_actions import send_typing_action
from django_telegram.functions.decorators import (
    restricted_group_id, restricted_group_member
)
from group_admin.bot_commands.group_admin import (
    set_bot_language as cmd_set_bot_language,
    member_join as cmd_member_join,
    member_exit as cmd_member_exit,
    welcome_button_handler_c as cmd_welcome_button_handler_c,
    AGREE_BTN_CALLBACK_DATA
)

logger = logging.getLogger('django')

BOT_TOKEN = settings.PROTO_BOT_TOKEN
GROUP_ID = settings.PROTO_GROUP_ID


@send_typing_action
@restricted_group_member(
    group_id=GROUP_ID,
    member_status=CHATMEMBER_ADMINISTRATOR,
    private_chat=False
)
def set_bot_language(update: Update, context: CallbackContext) -> None:
    set_language(BOT_TOKEN)
    cmd_set_bot_language(update, context, token=BOT_TOKEN)


@restricted_group_id(
    group_id=GROUP_ID
)
def member_join(update: Update, context: CallbackContext):
    cmd_member_join(update, context, GROUP_ID)


def member_exit(update: Update, context: CallbackContext):
    cmd_member_exit(update, context, GROUP_ID)


def welcome_button_handler_c(update: Update, context: CallbackContext):
    cmd_welcome_button_handler_c(update, context, GROUP_ID)


# Listen for when new members join group.
member_join_handler = MessageHandler(
    Filters.status_update.new_chat_members,
    member_join
)


# # Listen for when members leave group.
member_exit_handler = MessageHandler(
    Filters.status_update.left_chat_member,
    member_exit
)


welcome_button_handler = CallbackQueryHandler(
    welcome_button_handler_c,
    pattern='^' + AGREE_BTN_CALLBACK_DATA
)