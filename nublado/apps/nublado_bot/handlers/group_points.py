import re

from telegram import Update
from telegram.ext import ContextTypes, filters

from django.utils.translation import gettext as _

from django_telegram.utils import get_username_or_name, safe_reply
from django_telegram.models import (
    TelegramChat,
    TelegramUser,
    TelegramGroupMember,
)
from django_telegram.filters import TEXT_ONLY
from ..bot_messages import BOT_MESSAGES

# singular
POINT_NAME = "bot.nublado.point_name"
# plural
POINTS_NAME = "bot.nublado.points_name"
POINT_SYMBOL = "+"
MIN_POINT_SYMBOLS = 2
MAX_POINT_SYMBOLS = 3

# Map number of point symbols to respective number of points.
POINTS_MAP = {
    2: 1,
    3: 2,
    4: 4,
}

escaped_point_symbol = re.escape(POINT_SYMBOL)
POINT_FILTER = (
    TEXT_ONLY
    & filters.ChatType.GROUPS
    & filters.Regex(
        rf"^{escaped_point_symbol}{{{MIN_POINT_SYMBOLS},{MAX_POINT_SYMBOLS}}}"
    )
)


async def give_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Give points to another group member by replying to his or her message
    with a message prefixed by a specified symbol(s) (e.g., ++).

    ++ Thanks for the correction!
    """

    # Variables prefixed with tg are from Telegram.
    tg_message = update.effective_message
    tg_chat = update.effective_chat

    # The user sending the point(s).
    tg_sender_user = update.effective_user

    # The message must be a reply.
    if not tg_message or not tg_message.reply_to_message:
        return

    # The user receiving the point(s).
    tg_receiver_user = tg_message.reply_to_message.from_user

    # Text must start with the minimun number of point symbols.
    raw_text = tg_message.text or ""
    text = raw_text.strip()
    if not text.startswith(POINT_SYMBOL * MIN_POINT_SYMBOLS):
        return

    # Prevent giving points to self.
    if tg_sender_user.id == tg_receiver_user.id:
        bot_message = _(BOT_MESSAGES["no_give_self"]).format(points_name=_(POINTS_NAME))
        await safe_reply(update, bot_message)
        return

    # Prevent giving points to bots.
    if tg_receiver_user.is_bot:
        bot_message = _(BOT_MESSAGES["no_give_bot"]).format(points_name=_(POINTS_NAME))
        await safe_reply(update, bot_message)
        return

    # Get the number of point symbols at the beginning of the message.
    point_symbol_count = len(text) - len(text.lstrip(POINT_SYMBOL))
    if point_symbol_count not in POINTS_MAP:
        return

    # The number of points for the respective number of point symbols.
    num_points = POINTS_MAP[point_symbol_count]

    # Database

    # TelegramChat
    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)

    # TelegramUser
    sender_user = await TelegramUser.objects.aget_or_create_from_telegram_user(
        tg_sender_user
    )
    receiver_user = await TelegramUser.objects.aget_or_create_from_telegram_user(
        tg_receiver_user
    )

    # TelegramGroupMember
    sender_member, sender_created = await TelegramGroupMember.objects.aget_or_create(
        user=sender_user,
        chat=chat,
    )
    receiver_member, receiver_created = (
        await TelegramGroupMember.objects.aget_or_create(
            user=receiver_user,
            chat=chat,
        )
    )

    # Increment points
    receiver_member.points += num_points
    await receiver_member.asave()

    if num_points > 1:
        bot_message = _(BOT_MESSAGES["give_points"]).format(
            sender_name=get_username_or_name(tg_sender_user),
            sender_points=sender_member.points,
            num_points=num_points,
            points_name=_(POINTS_NAME),
            receiver_name=get_username_or_name(tg_receiver_user),
            receiver_points=receiver_member.points,
        )
    else:
        bot_message = _(BOT_MESSAGES["give_point"]).format(
            sender_name=get_username_or_name(tg_sender_user),
            sender_points=sender_member.points,
            points_name=_(POINT_NAME),
            receiver_name=get_username_or_name(tg_receiver_user),
            receiver_points=receiver_member.points,
        )

    await safe_reply(update, bot_message)
