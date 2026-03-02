import re
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from django.utils.translation import gettext_lazy as _

from group_points.point_engine import PointsEngine
from group_points.services import transfer_points
from group_points.constants import PointTransferError

from django_telegram.utils.helpers import get_username_or_name, safe_reply
from ..constants import POINT_SYMBOL, DEFAULT_POINTS_MAP, POINT_NAME, POINTS_NAME
from ..bot_messages import BOT_MESSAGES

# Filter for group text messages starting with point symbols
escaped_point_symbol = re.escape(POINT_SYMBOL)
POINT_FILTER = (
    filters.TEXT
    & ~filters.COMMAND
    & filters.ChatType.GROUPS
    & filters.UpdateType.MESSAGE
    & filters.Regex(rf"^{escaped_point_symbol}+")
)

async def give_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_message = update.effective_message
    tg_chat = update.effective_chat
    tg_sender = update.effective_user

    if not tg_message or not tg_message.reply_to_message:
        return

    tg_receiver = tg_message.reply_to_message.from_user

    # Initialize engine per bot config
    points_engine = PointsEngine(point_symbol=POINT_SYMBOL, points_map=DEFAULT_POINTS_MAP)

    # Validate transfer
    error = points_engine.validate_point_transfer(tg_sender, tg_receiver)
    if error == PointTransferError.SELF:
        await safe_reply(update, context, BOT_MESSAGES["no_give_self"], points_name=_(POINTS_NAME))
        return
    if error == PointTransferError.BOT:
        await safe_reply(update, context, BOT_MESSAGES["no_give_bot"], points_name=_(POINTS_NAME))
        return

    # Extract number of points
    num_points = points_engine.extract_points(tg_message.text)
    if not num_points:
        return

    # Persist points
    sender_member, receiver_member = await transfer_points(tg_chat, tg_sender, tg_receiver, num_points)

    # Reply with bot-specific message
    if num_points > 1:
        await safe_reply(
            update,
            context,
            BOT_MESSAGES["give_points"],
            sender_name=get_username_or_name(tg_sender),
            sender_points=sender_member.points,
            num_points=num_points,
            points_name=_(POINTS_NAME),
            receiver_name=get_username_or_name(tg_receiver),
            receiver_points=receiver_member.points,
        )
    else:
        await safe_reply(
            update,
            context,
            BOT_MESSAGES["give_point"],
            sender_name=get_username_or_name(tg_sender),
            sender_points=sender_member.points,
            points_name=_(POINT_NAME),
            receiver_name=get_username_or_name(tg_receiver),
            receiver_points=receiver_member.points,
        )