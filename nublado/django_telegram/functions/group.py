import logging
import random

from asgiref.sync import sync_to_async
from telegram import Update, Bot
from telegram.helpers import escape_markdown
from telegram.constants import ChatMemberStatus
from telegram.constants import ChatType

from django.conf import settings

from ..models import GroupMember

logger = logging.getLogger('django')

# Member status is in ascending order.
GROUP_MEMBERS = {
    ChatMemberStatus.MEMBER: 1,
    ChatMemberStatus.ADMINISTRATOR: 2,
    ChatMemberStatus.OWNER: 3
}
GROUP_TYPES = [
    ChatType.GROUP,
    ChatType.SUPERGROUP
]

@sync_to_async
def get_random_group_member(group_id: int):
    members = GroupMember.objects.filter(group_id=group_id)
    if members.count() > 0:
        index = random.randint(0, len(members) - 1)
        return members[index]
    else:
        return None


async def get_chat_member(bot: Bot, user_id: int, chat_id: int):
    try:
        chat_member = await bot.get_chat_member(
            chat_id, user_id
        )
        return chat_member
    except Exception as e:
        logger.error(e)
        return None


async def is_group_chat(bot: Bot, chat_id: int) -> bool:
    """Return whether chat is a group chat."""
    try:
        chat = await bot.get_chat(chat_id)
        return chat.type in GROUP_TYPES
    except Exception as e:
        logger.error(e)
        logger.warn(f"Chat {chat_id} isn't a group.")
        return False


async def is_group_id(bot: Bot, chat_id: int, group_id: int) -> bool:
    """Returns whether chat is a specific group chat by id"""
    return await is_group_chat(bot, chat_id) and chat_id == group_id



async def is_member_status(
        bot: Bot,
        user_id: int,
        group_id: int,
        member_status: str = ChatMemberStatus.MEMBER
):
    if member_status in GROUP_MEMBERS.keys():
        chat_member = await get_chat_member(bot, user_id, group_id)
        if chat_member:
            if chat_member.status in GROUP_MEMBERS.keys():
                return GROUP_MEMBERS[chat_member.status] >= GROUP_MEMBERS[member_status]
            else:
                logger.warn(f"Chat member status {chat_member.status} not in GROUP_MEMBERS.")
                return False
        else:
            logger.warn("Non chat member.")
            return False
    else:
        logger.warn("Target member status not in GROUP_MEMBERS.")
        return False


def send_non_member_message(update: Update, bot: Bot, group_id: int) -> None:
    try:
        group = bot.get_chat(group_id)
        invite_link = escape_markdown(group.invite_link)
        message = f"This bot is exclusively for members of the group\n*{group.title}*." \
        f"\n\nCome join us!\n{invite_link}"
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=message
        )
    except Exception as e:
        logger.error(e)
        return
