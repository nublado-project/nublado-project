import logging

import pytest
from telethon import events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.utils import get_display_name

from django.conf import settings
from django.db import connection
from django.utils.translation import gettext as _

from django_telegram.models import GroupMember
from group_admin.bot_commands.group_admin import (
    BOT_MESSAGES, add_member
)
from .helpers import (
    get_button_with_text, is_group_member
)
from .conftest import (
    TEST_GROUP_ID, TEST_BOT_ID, TIMEOUT, MAX_MSGS
)

TEST_GROUP_INVITATION = "elL0E4yk9vs3ZGZh"

logger = logging.getLogger('django')
logger_debug = logging.getLogger('django-debug')

# Note: Suspend the external webhook web service and run the bot
# locally with polling when running these tests.
# python manage.py runbot testbot --settings=config.settings.test


class TestGroupAdminCommands:
    @pytest.mark.django_db(transaction=True)
    @pytest.mark.asyncio
    async def test_member_join_group(self, tg_client):
        # Self user
        me = await tg_client.get_me()

        # Leave the group if already a memeber.
        if await is_group_member(tg_client, TEST_GROUP_ID):
            await tg_client.delete_dialog(TEST_GROUP_ID)

        # Pending: Check if member not in group.

        # Join the group.
        updates = await tg_client(ImportChatInviteRequest(TEST_GROUP_INVITATION))

        # Pending: Check if new member can send messages before pressing the confirmation button.

        # Conversation in group
        async with tg_client.conversation(
            TEST_GROUP_ID,
            timeout=TIMEOUT,
            max_messages=MAX_MSGS
        ) as conv:
            # Get the welcome message with the confirmation button.
            response = await conv.wait_event(
                events.NewMessage(incoming=True, from_users=TEST_BOT_ID)
            )
            greeting = f"Welcome to the group, {get_display_name(me)}"
            welcome_msg = "Please read the following rules " \
                          "and click the \"I agree\" button"
            assert greeting in response.raw_text
            assert welcome_msg in response.raw_text
            button = get_button_with_text(response.message, "I agree.")
            assert button is not None
            await button.click()
            # Get the welcome message after the user has clicked the confirmation button.
            response = await conv.wait_event(
                events.NewMessage(incoming=True, from_users=TEST_BOT_ID)
            )
            welcome_msg = "We require new members to introduce themselves " \
                          "with a voice message."
            assert greeting in response.raw_text
            assert welcome_msg in response.raw_text
            db_name = connection.get_connection_params()
            logger.info(f"db: {db_name}")

            group_member = await GroupMember.objects.a_get_group_member(TEST_GROUP_ID, me.id)
            assert group_member is None

            # Pending: Check if new member can send messages after clicking 
            # the confirmation button.
