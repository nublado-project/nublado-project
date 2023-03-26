import datetime as dt
import logging

from asgiref.sync import sync_to_async

from telegram import (
    Bot, Update, ChatPermissions,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ContextTypes
)
from telegram.constants import ChatMemberStatus

from django.utils.translation import activate, gettext as _
from django.conf import settings

from django_telegram.models import GroupMember, BotConfig
from django_telegram.functions.admin import (
    update_group_members_from_admins,
    get_non_group_members,
)
from django_telegram.models import GroupMember

logger = logging.getLogger('django')

# Translated strings.
BOT_MESSAGES = {
    'agree': _("I agree."),
    'welcome': _(
        "Welcome to the group, {name}.\n\n" \
        "Please read the following rules and click the \"I agree\" button to participate.\n\n" \
        "*Rules*\n" \
        "- Communicate in only English and Spanish.\n" \
        "- Be a good example. Help others out with corrections."
    ),
    'welcome_agreed': _(
        "Welcome to the group, {name}.\n\n" \
        "*YOU NEED TO INTRODUCE YOURSELF WITH A VOICE MESSAGE.*\n\n" \
        "This is our our protocol for new members. It helps us filter out fake accounts, trolls, etc.\n\n" \
        "We look forward to hearing from you."
    ),
    'bot_language_set': _("The bot's language has been changed to {language}."),
    'error_invalid_language_key': _("Error: The possible language keys are [{language_keys}].")
}

# Constants
AGREE_BTN_CALLBACK_DATA = "chat_member_welcome_agree"
PENDING_VERIFICATION_TAG = "#pending\_verification"


async def set_bot_language(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    token: str
):
    if len(context.args) >= 1:
        lang = str(context.args[0])
        if lang in settings.LANGUAGES_DICT.keys():
            if token in settings.DJANGO_TELEGRAM['bots'].keys():
                bot_config, bot_config_created = await BotConfig.objects.aget_or_create(
                    id=token
                )
                if bot_config.language != lang:
                    bot_config.language = lang
                    await sync_to_async(bot_config.save)()
                activate(lang)
                message = _(BOT_MESSAGES['bot_language_set']).format(
                    language=_(settings.LANGUAGES_DICT[lang])
                )
            else:
                logger.error(f"Bot {token} not found in the configuration.")
        else:
            keys = list(settings.LANGUAGES_DICT.keys())
            message = _(BOT_MESSAGES['error_invalid_language_key']).format(
                language_keys=keys
            )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


# @send_typing_action
# @restricted_group_member(
#     group_id=GROUP_ID,
#     member_status=ChatMemberStatus.OWNER,
#     group_chat=False
# )
# async def get_non_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await get_non_group_members(context.bot, GROUP_ID)


# @send_typing_action
# @restricted_group_member(
#     group_id=GROUP_ID,
#     member_status=ChatMemberStatus.OWNER,
#     group_chat=False
# )
# async def update_group_admins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     members = update_group_members_from_admins(context.bot, GROUP_ID)
#     if members:
#         message = _("Group members updated from admins.")
#     else:
#         message = _("Group members not updated from admins.")

#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text=message
#     )


async def has_member(group_id: int, user_id: int) -> bool:
    member_exists = await GroupMember.objects.filter(
        group_id=group_id,
        user_id=user_id
    ).aexists()
    return member_exists


async def add_member(group_id, user_id):
    member_exists = await has_member(group_id, user_id)
    member = await GroupMember.objects.a_get_group_member(group_id, user_id)
    if not member_exists:
        await sync_to_async(GroupMember.objects.create_group_member)(
            group_id=group_id,
            user_id=user_id
        )
    member_exists = await has_member(group_id, user_id)
    member = await GroupMember.objects.a_get_group_member(group_id, user_id)


async def remove_member(user_id, group_id):
    await GroupMember.objects.filter(
        group_id=group_id,
        user_id=user_id
    ).adelete()


async def restrict_chat_member(bot: Bot, user_id: int, chat_id: int):
    try:
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False  
        )
        await bot.restrict_chat_member(
            user_id=user_id,
            chat_id=chat_id,
            permissions=permissions 
        )
        return True
    except:
        logger.error(f"Error disactivating member {user_id}")
        return False


async def unrestrict_chat_member(
    bot: Bot,
    user_id: int,
    chat_id: int,
    interval_minutes: int = 1
):
    """Restore restricted chat member to group's default member permissions."""
    try:
        chat = await bot.get_chat(chat_id)
        permissions = chat.permissions
        date_now = dt.datetime.now()
        date_until = date_now + dt.timedelta(minutes=interval_minutes)
        await bot.restrict_chat_member(
            user_id=user_id,
            chat_id=chat_id,
            permissions=permissions,
            until_date=date_until
        )
        return True
    except:
        logger.error(f"Error unrestricting member {user_id}")
        return False


async def member_join(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int
):
    if update.message.new_chat_members:
        for user in update.message.new_chat_members:
            # Add user to db
            await add_member(group_id, user.id)
            # Mute user until he or she presses the "I agree" button.
            await restrict_chat_member(context.bot, user.id, group_id)
            callback_data = AGREE_BTN_CALLBACK_DATA + " " + str(user.id)
            keyboard = [
                [
                    InlineKeyboardButton(
                        _(BOT_MESSAGES['agree']),
                        callback_data=callback_data
                    ),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            message = _(BOT_MESSAGES['welcome']).format(
                name=user.mention_markdown()
            )
            await context.bot.send_message(
                text=message,
                chat_id=group_id,
                reply_markup=reply_markup
            )
        # Delete service message.
        try:
            await context.bot.delete_message(
                message_id=update.message.message_id,
                chat_id=update.effective_chat.id
            )
        except:
            pass


async def member_exit(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int
):
    if update.message.left_chat_member:
        user = update.message.left_chat_member
        # Delete member from db.
        await remove_member(user.id, group_id)
        # Delete service message.
        try:
            await context.bot.delete_message(
                message_id=update.message.message_id,
                chat_id=update.effective_chat.id
            )
        except:
            pass


# # Listen for when new members join group.
# member_join_handler = MessageHandler(
#     Filters.status_update.new_chat_members,
#     member_join
# )


# # Listen for when members leave group.
# member_exit_handler = MessageHandler(
#     Filters.status_update.left_chat_member,
#     member_exit
# )


async def chat_member_welcome_agree(
    bot: Bot, user_id: int, chat_id: int, welcome_message_id: int = None
) -> None:
    await unrestrict_chat_member(bot, user_id, chat_id)
    if welcome_message_id:
        try:
            await bot.delete_message(
                message_id=welcome_message_id,
                chat_id=chat_id
            )
        except:
            logger.error(f"Error tring to delete  welcome message {welcome_message_id}.")
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        message = _(BOT_MESSAGES['welcome_agreed']).format(
            name=member.user.mention_markdown()
        )
        welcome_message = await bot.send_message(
            chat_id=chat_id,
            text=message
        )
        await bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=welcome_message.message_id,
            text=PENDING_VERIFICATION_TAG
        )
    except Exception as e:
        logger.error(e)


async def welcome_button_handler_c(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int
):
    """Parse the CallbackQuery and perform corresponding actions."""
    query = update.callback_query
    await query.answer()
    data = query.data.split(" ")
    if len(data) >= 2:
        if data[0] == AGREE_BTN_CALLBACK_DATA:
            user_id = int(data[1])
            # Check if effective user is the user that clicked the button.
            if update.effective_user.id == user_id:
                await chat_member_welcome_agree(
                    context.bot,
                    user_id,
                    group_id,
                    query.message.message_id
                )
            else:
                logger.info("Another user clicked the welcome buttton.")
    else:
       await query.edit_message_text(text=f"Selected option: {query.data}")


# welcome_button_handler = CallbackQueryHandler(
#     welcome_button_handler_c,
#     pattern='^' + AGREE_BTN_CALLBACK_DATA
# )
