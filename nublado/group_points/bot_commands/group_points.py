import logging

from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import (
    ContextTypes, MessageHandler, filters
)
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from django_telegram.models import GroupMember
from django_telegram.functions.user import get_username_or_name
from ..bot_messages import BOT_MESSAGES

logger = logging.getLogger('django')

ADD_POINTS_TRIGGER = '+'
ADD_POINTS_REGEX = '^[' + ADD_POINTS_TRIGGER + '][\s\S]*$'
REMOVE_POINTS_TRIGGER = '-'
REMOVE_POINTS_REGEX = '^[' + REMOVE_POINTS_TRIGGER + '][\s\S]*$'
POINT_NAME = "bot.point_name"
POINTS_NAME = "bot.points_name"
TOP_POINTS_LIMIT = 10


@sync_to_async
def get_or_create_group_member(user_id, group_id):
    """Get or create group member from db."""
    group_member, group_member_created = GroupMember.objects.get_or_create(
        group_id=group_id,
        user_id=user_id
    )

    return group_member


async def add_points(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    num_points: int = 1,
    group_id: int = None,
    point_name: str = None,
    points_name: str = None,
) -> None:
    if group_id:
        # Check if the message is a reply to another message.
        if update.message.reply_to_message:
            sender = update.effective_user
            receiver = update.message.reply_to_message.from_user

            # Check if the reply is to another member and not a bot or oneself.
            if not receiver.is_bot and sender != receiver:
                member_sender = await get_or_create_group_member(sender.id, group_id)
                member_receiver = await get_or_create_group_member(receiver.id, group_id)
                member_receiver.points += num_points
                await sync_to_async(member_receiver.save)()

                if point_name is None:
                    point_name = POINT_NAME
                if points_name is None:
                    points_name = POINTS_NAME

                if num_points > 1:
                    bot_message = _(BOT_MESSAGES['give_points']).format(
                        sender_name=sender.mention_markdown(),
                        sender_points=member_sender.points,
                        num_points=num_points,
                        points_name=_(points_name),
                        receiver_name=receiver.mention_markdown(),
                        receiver_points=member_receiver.points
                    )
                else:
                    bot_message = _(BOT_MESSAGES['give_point']).format(
                        sender_name=sender.mention_markdown(),
                        sender_points=member_sender.points,
                        points_name=_(point_name),
                        receiver_name=receiver.mention_markdown(),
                        receiver_points=member_receiver.points
                    )
                await context.bot.send_message(
                    chat_id=group_id,
                    text=bot_message
                )

            elif receiver.is_bot:
                bot_message = _(BOT_MESSAGES['no_give_bot']).format(
                    points_name=_(points_name)
                )
                await update.message.reply_text(text=bot_message)

            elif receiver == sender:
                bot_message = _(BOT_MESSAGES['no_give_self']).format(
                    points_name=_(points_name)
                )
                await update.message.reply_text(text=bot_message)


async def remove_points(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    num_points: int = 1,
    group_id: int = None,
    point_name: str = None,
    points_name: str = None
) -> None:
    if group_id:
        if update.message.reply_to_message:
            sender = update.effective_user
            receiver = update.message.reply_to_message.from_user

            if not receiver.is_bot and sender != receiver:
                # Fetch members from project database.
                member_sender = await get_or_create_group_member(sender.id, group_id)
                member_receiver = await get_or_create_group_member(receiver.id, group_id)
                points = member_receiver.points - num_points
                member_receiver.points = points if points >= 0 else 0
                await sync_to_async(member_receiver.save)()

                if point_name is None:
                    point_name = POINT_NAME
                if points_name is None:
                    points_name = POINTS_NAME

                if num_points > 1:
                    bot_message = _(BOT_MESSAGES['take_points']).format(
                        sender_name=sender.mention_markdown(),
                        sender_points=member_sender.points,
                        num_points=num_points,
                        points_name=_(points_name),
                        receiver_name=receiver.mention_markdown(),
                        receiver_points=member_receiver.points
                    )
                else:
                    bot_message = _(BOT_MESSAGES['take_point']).format(
                        sender_name=sender.mention_markdown(),
                        sender_points=member_sender.points,
                        points_name=_(point_name),
                        receiver_name=receiver.mention_markdown(),
                        receiver_points=member_receiver.points
                    )
                await context.bot.send_message(
                    chat_id=group_id,
                    text=bot_message
                )
            elif receiver.is_bot:
                bot_message = _(BOT_MESSAGES['no_take_bot']).format(
                    points_name=_(points_name)
                )
                await update.message.reply_text(text=bot_message)
            elif receiver == sender:
                bot_message = _(BOT_MESSAGES['no_take_self']).format(
                    points_name=_(points_name)
                )
                await update.message.reply_text(text=bot_message)


# Message handlers to listen for triggers to add or remove points.
add_points_handler = MessageHandler(
    (filters.Regex(ADD_POINTS_REGEX) & filters.REPLY),
    add_points
)


remove_points_handler = MessageHandler(
    (filters.Regex(REMOVE_POINTS_REGEX) & filters.REPLY),
    remove_points
)