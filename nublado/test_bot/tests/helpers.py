import re
from typing import Optional
import logging

from telethon import TelegramClient
from telethon.tl.custom.message import Message, MessageButton
from telethon.tl.types import PeerUser

logger_debug = logging.getLogger('django-debug')


def is_from_test_bot(message: Message, test_bot_id: int) -> bool:
    logger_debug.info(message.from_id)
    return (isinstance(message.from_id, PeerUser) and
            message.from_id.user_id == test_bot_id)


async def is_group_member(
    client: TelegramClient,
    group_id: int
) -> bool:
    async for dialog in client.iter_dialogs():
        if hasattr(dialog.entity, 'megagroup') and dialog.entity.megagroup:
            id = int(f"-100{dialog.entity.id}")
            if id == group_id:
                return True
    return False


def get_num_list_from_str(txt: str):
    """
    Return a list of comma-separated numbers in string.
    Example: "Hello 1, 2, 3 world" -> ['1', '2', '3]
             "Hello 1 world." -> ['1']
    """
    num_list = re.findall("\d+(?:,\d+)?", txt)
    return num_list


def get_button_with_text(
    message: Message, text: str, strict: bool = False
) -> Optional[MessageButton]:
    """Return MessageButton from Message with specified text or None."""
    if message.buttons is None:
        return None

    for row in message.buttons:
        for button in row:
            if strict:
                is_match = text == button.text
            else:
                is_match = text in button.text
            if is_match:
                return button

    return None