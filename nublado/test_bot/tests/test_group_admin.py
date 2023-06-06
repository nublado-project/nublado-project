import logging

import pytest
from telethon import events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.utils import get_display_name

from django.conf import settings
from django.utils.translation import gettext as _

from django_telegram.models import GroupMember
from .helpers import (
    get_button_with_text, is_group_member
)
from .helpers import (
    is_from_test_bot
)
from .conftest import (
    TEST_GROUP_ID, TEST_BOT_ID, TIMEOUT, MAX_MSGS
)

TEST_GROUP_INVITATION = "elL0E4yk9vs3ZGZh"

logger = logging.getLogger('django')
logger_debug = logging.getLogger('django-debug')


class TestGroupAdminCommands:

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.asyncio
    async def test_set_bot_language(self, group_conv):

        # Note: Requires admin
        cmd = "/set_bot_language"
        cmd_test_output = "/test_bot"

        # English
        await group_conv.send_message(f"{cmd} es")
        resp = await group_conv.get_response()
        assert is_from_test_bot(resp, TEST_BOT_ID)
        assert "El idioma del bot ha sido cambiado al español" in resp.raw_text
        await group_conv.send_message(cmd_test_output)
        resp = await group_conv.get_response()
        assert "probando probando" in resp.raw_text

        # Spanish
        await group_conv.send_message(f"{cmd} en")
        resp = await group_conv.get_response()
        assert is_from_test_bot(resp, TEST_BOT_ID)
        assert "The bot's language has been changed to English" in resp.raw_text
        await group_conv.send_message(cmd_test_output)
        resp = await group_conv.get_response()
        assert "testing testing" in resp.raw_text

        # Non-supported language
        await group_conv.send_message(f"{cmd} xx")
        resp = await group_conv.get_response()
        assert is_from_test_bot(resp, TEST_BOT_ID)
        assert "Error: The possible language keys are ['en', 'es']" in resp.raw_text
    

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.asyncio
    async def test_member_join_group(self, tg_client):
        # Self user
        me = await tg_client.get_me()

        # Leave the group if already a memeber.
        if await is_group_member(tg_client, TEST_GROUP_ID):
            await tg_client.delete_dialog(TEST_GROUP_ID)

        # Check if member not in db.
        group_member = await GroupMember.objects.a_get_group_member(TEST_GROUP_ID, me.id)
        assert group_member is None

        # Join the group.
        updates = await tg_client(ImportChatInviteRequest(TEST_GROUP_INVITATION))

        # Pending: Check if new member can send messages before pressing the confirmation button.
        permissions = await tg_client.get_permissions(TEST_GROUP_ID, me.id)

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
            welcome_msg = "YOU NEED TO INTRODUCE YOURSELF WITH A VOICE MESSAGE OR YOU WILL BE " \
                          "BOOTED FROM THE GROUP.\n\nThis is our our protocol for new members. " \
                          "It helps us filter out fake accounts, trolls, etc.\n\nWe look forward to hearing from you."
            assert greeting in response.raw_text
            assert welcome_msg in response.raw_text

            # Check if member has been added to the db.
            group_member = await GroupMember.objects.a_get_group_member(TEST_GROUP_ID, me.id)
            assert group_member is not None

            # Pending: Check if new member can send messages after clicking 
            # the confirmation button.
            permissions = await tg_client.get_permissions(TEST_GROUP_ID, me.id)
