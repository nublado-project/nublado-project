import logging
import asyncio

import pytest
import pytest_asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

from django.conf import settings

dt = settings.DJANGO_TELEGRAM['testing']
TEST_BOT_ID = 5863994740
API_ID = dt['api_id']
API_HASH = dt['api_hash']
SESSION_STR = dt['api_session_str']
TEST_GROUP_ID = settings.TEST_GROUP_ID
TIMEOUT = 5
MAX_MSGS = 10000
USER_B_ID = settings.TEST_GROUP_OWNER_ID

logger = logging.getLogger('django')


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def tg_client():
    client = TelegramClient(
        StringSession(SESSION_STR),
        API_ID,
        API_HASH,
        sequential_updates=True
    )  
    await client.start()
    await client.get_me()
    await client.get_dialogs()
    yield client
    await client.disconnect()
    await client.disconnected


@pytest_asyncio.fixture()
async def group_conv(tg_client):
    """Open a conversation with the bot."""
    async with tg_client.conversation(
        TEST_GROUP_ID,
        timeout=TIMEOUT,
        max_messages=MAX_MSGS
    ) as conv:
        yield conv
