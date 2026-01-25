from telegram import Update, User
from telegram.ext import ContextTypes

from django.utils.translation import gettext_lazy as _

from django_telegram.models import (
    TelegramChat,
    TelegramUser,
    TelegramGroupMember,
)
from django_telegram.permissions import group_only

# singular
POINT_NAME = "raindrop"
# plural
POINTS_NAME = "raindrops"
POINT_SYMBOL = "+"
MIN_POINT_SYMBOLS = 2
MAX_POINT_SYMBOLS = 3

# Map number of point symbols to respective number of points.
POINTS_MAP = {
    2: 1,
    3: 2,
}

# Bot messages
msg_no_give_points_self = _("You can't give {points_name} to yourself.")
msg_no_give_points_bot = _("You can't give {points_name} to a bot.")
msg_give_point = _(
    "{sender_name} ({sender_points}) has given a " + \
    "{points_name} to {receiver_name} ({receiver_points})."
)
msg_give_points = _(
    "{sender_name} ({sender_points}) has given {num_points} " + \
    "{points_name} to {receiver_name} ({receiver_points})."
)


def get_username_or_name(user: User) -> str:
    """Return user's username or first and last names."""
    if user.username:
        return user.username
    elif user.last_name:
        return f"{user.first_name} {user.last_name}"
    else:
        return user.first_name


@group_only
async def give_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    tg_chat = update.effective_chat

    # The user sending the point(s).
    tg_sender_user = update.effective_user

    # Must be a reply.
    if not message.reply_to_message:
        return

    # The user receiving the point(s).
    tg_receiver_user = message.reply_to_message.from_user

   # Prevent giving points to self.
    if tg_sender_user.id == tg_receiver_user.id:
        reply_message = _(msg_no_give_points_self).format(
            points_name=_(POINTS_NAME)
        )     
        await message.reply_text(reply_message)
        return

    # Prevent giving points to bots.
    if tg_receiver_user.is_bot:
        reply_message = _(msg_no_give_points_bot).format(
            points_name=_(POINTS_NAME)
        )  
        await message.reply_text(reply_message)
        return

    # Text must start with the minimun number of point symbols.
    text = message.text.strip()
    if not text or not text.startswith(POINT_SYMBOL * MIN_POINT_SYMBOLS):
        return

    point_symbol_count = len(text) - len(text.lstrip(POINT_SYMBOL))
    if point_symbol_count not in POINTS_MAP:
        return

    num_points = POINTS_MAP[point_symbol_count]

    # Database

    # TelegramChat
    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)
    
    # TelegramUser
    sender_user = await TelegramUser.objects.aget_or_create_from_telegram_user(tg_sender_user)
    receiver_user = await TelegramUser.objects.aget_or_create_from_telegram_user(tg_receiver_user)

    # TelegramGroupMember
    sender_member, created = await TelegramGroupMember.objects.aget_or_create(
        user=sender_user,
        chat=chat,
    )
    receiver_member, created = await TelegramGroupMember.objects.aget_or_create(
        user=receiver_user,
        chat=chat,
    )

    # Increment points
    receiver_member.points += num_points
    await receiver_member.asave()

    if num_points > 1:
        reply_message = _(msg_give_points).format(
            sender_name=get_username_or_name(tg_sender_user),
            sender_points=sender_member.points,
            num_points=num_points,
            points_name=_(POINTS_NAME),
            receiver_name=get_username_or_name(tg_receiver_user),
            receiver_points=receiver_member.points
        )
    else:
        reply_message = _(msg_give_point).format(
            sender_name=get_username_or_name(tg_sender_user),
            sender_points=sender_member.points,
            points_name=_(POINT_NAME),
            receiver_name=get_username_or_name(tg_receiver_user),
            receiver_points=receiver_member.points
        )

    await message.reply_text(reply_message)
