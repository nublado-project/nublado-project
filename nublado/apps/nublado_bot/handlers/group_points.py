from telegram import Update, User
from telegram.ext import ContextTypes

from django.utils.translation import gettext as _

from django_telegram.models import (
    TelegramChat,
    TelegramUser,
    TelegramGroupMember,
)

from django_telegram.policies import GroupOnly
from django_telegram.handlers import BaseTelegramHandler

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

BOT_MESSAGES = {
    "no_give_bot": "bot.message.no_give_points_bot {points_name}",
    # "no_take_bot": _("bot.message.no_take_points_bot {points_name}"),
    "no_give_self": "bot.message.no_give_points_self {points_name}",
    # "no_take_self": _("bot.message.no_take_points_self {points_name}"),
    "give_point":
        "bot.message.give_point_member {sender_name} {sender_points} "
        + "{points_name} {receiver_name} {receiver_points}"
    ,
    "give_points":
        "bot.message.give_points_member {sender_name} {sender_points} {num_points} "
        + "{points_name} {receiver_name} {receiver_points}"
    ,
    # "take_point": _(
    #     "bot.message.take_point_member {sender_name} {sender_points} " + \
    #     "{points_name} {receiver_name} {receiver_points}"
    # ),
    # "take_points": _(
    #     "bot.message.take_points_member {sender_name} {sender_points} {num_points} " + \
    #     "{points_name} {receiver_name} {receiver_points}"
    # ),
}


def get_username_or_name(user: User) -> str:
    """Return user's username or first and last names."""
    if user.username:
        return user.username
    elif user.last_name:
        return f"{user.first_name} {user.last_name}"
    else:
        return user.first_name

class GivePointsHandler(BaseTelegramHandler):
    policies = [GroupOnly()]

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        if not tg_message.reply_to_message:
            return

        # The user receiving the point(s).
        tg_receiver_user = tg_message.reply_to_message.from_user

        # Text must start with the minimun number of point symbols.
        text = tg_message.text.strip()
        if not text or not text.startswith(POINT_SYMBOL * MIN_POINT_SYMBOLS):
            return

        # Prevent giving points to self.
        if tg_sender_user.id == tg_receiver_user.id:
            bot_message = _(BOT_MESSAGES["no_give_self"]).format(
                points_name=_(POINTS_NAME)
            )
            await tg_message.reply_text(bot_message)
            return

        # Prevent giving points to bots.
        if tg_receiver_user.is_bot:
            bot_message = _(BOT_MESSAGES["no_give_bot"]).format(points_name=_(POINTS_NAME))
            await tg_message.reply_text(bot_message)
            return

        point_symbol_count = len(text) - len(text.lstrip(POINT_SYMBOL))
        if point_symbol_count not in POINTS_MAP:
            return

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

        await tg_message.reply_text(bot_message)
