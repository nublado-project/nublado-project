import logging

import pytest
from telethon.utils import get_display_name

from django.conf import settings
from django.utils.translation import gettext as _

from bot_misc.bot_commands.misc import (
    MIN_DICE, MAX_DICE,
    BOT_MESSAGES as BOT_MISC_MESSAGES
)

from .helpers import (
    is_from_test_bot, get_num_list_from_str
)
from .conftest import (
    TEST_GROUP_ID, TEST_BOT_ID, TIMEOUT, MAX_MSGS
)

logger = logging.getLogger('django')

# Note: Suspend the external webhook web service and run the bot
# locally with polling when running these tests.
# python manage.py runbot testbot --settings=config.settings.test


class TestGroupNotesCommands:
    @pytest.mark.asyncio
    async def test_save_group_note(self, group_conv):
        cmd = "/save_group_note"
        await group_conv.send_message(cmd)
        resp = await group_conv.get_response()
        assert is_from_test_bot(resp, TEST_BOT_ID)
        assert "UTC" in resp.raw_text


