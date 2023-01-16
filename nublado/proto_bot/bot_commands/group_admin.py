import logging

from telegram import Update
from telegram.ext import (
    ContextTypes, CallbackQueryHandler,
    MessageHandler, filters
)
from telegram.constants import ChatMemberStatus

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
    member_status=ChatMemberStatus.ADMINISTRATOR,
    private_chat=False
)
async def set_bot_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await set_language(BOT_TOKEN)
    await cmd_set_bot_language(update, context, token=BOT_TOKEN)


@restricted_group_id(
    group_id=GROUP_ID
)
async def member_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_language(BOT_TOKEN)
    await cmd_member_join(update, context, GROUP_ID)

@restricted_group_id(
    group_id=GROUP_ID
)
async def member_exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_language(BOT_TOKEN)
    await cmd_member_exit(update, context, GROUP_ID)


async def welcome_button_handler_c(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_welcome_button_handler_c(update, context, GROUP_ID)


# Listen for when new members join group.
member_join_handler = MessageHandler(
    filters.StatusUpdate.NEW_CHAT_MEMBERS,
    member_join
)


# # Listen for when members leave group.
member_exit_handler = MessageHandler(
    filters.StatusUpdate.LEFT_CHAT_MEMBER,
    member_exit
)


welcome_button_handler = CallbackQueryHandler(
    welcome_button_handler_c,
    pattern='^' + AGREE_BTN_CALLBACK_DATA
)