from html import escape

from telegram import Update, User, Chat, ChatMember, Message
from telegram.ext import ContextTypes
from telegram.constants import ChatType, ChatMemberStatus

from django.utils.translation import override
from django.conf import settings

from ..constants import CONTEXT_LANGUAGE_KEY


# Helper functions
def _is_group(tg_chat: Chat):
    return tg_chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}


def _is_private(tg_chat: Chat):
    return tg_chat.type == ChatType.PRIVATE


def _is_admin(tg_member: ChatMember):
    return tg_member.status in [
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ]


def _is_group_owner(tg_member: ChatMember):
    return tg_member.status == ChatMemberStatus.OWNER


# def get_username_or_name(tg_user: User, prefer_username: bool = True):
#     """
#     Return user's @username or first and last names, if available.
#     """
#     # Display username with @ if preferred and user has a username.
#     if prefer_username and tg_user.username:
#         display_name = f"@{tg_user.username}"
#     else:
#         # Display the user's first and last names, if available, or fall back to 
#         # the user's first name.
#         if tg_user.last_name:
#             display_name = f"{tg_user.first_name} {tg_user.last_name}"
#         else:
#             display_name = tg_user.first_name

#     return display_name


def user_display_name(tg_user: User, prefer_username: bool = True, clickable: bool = True) -> str:
    """
    Return user's @username or first and last names, if available.
    Format the display name as a link if clickable == True.
    """
    # Display username with @ if preferred and user has a username.
    if prefer_username and tg_user.username:
        display_name = f"@{tg_user.username}"
    else:
        # Display the user's first and last names, if available, or fall back to 
        # the user's first name.
        if tg_user.last_name:
            display_name = f"{tg_user.first_name} {tg_user.last_name}"
        else:
            display_name = tg_user.first_name

    display_name = escape(display_name)

    if clickable:
        return f'<a href="tg://user?id={tg_user.id}">{display_name}</a>'

    return display_name


def message_link(tg_chat_id: str, tg_message_id: str):
    tg_chat_id = str(tg_chat_id)

    if tg_chat_id.startswith("-100"):
        tg_chat_id = tg_chat_id[4:]

    return f"https://t.me/c/{tg_chat_id}/{tg_message_id}"
    

def get_context_language(context: ContextTypes.DEFAULT_TYPE):
    return context.chat_data.get(CONTEXT_LANGUAGE_KEY, settings.LANGUAGE_CODE)


def set_context_language(
    context: ContextTypes.DEFAULT_TYPE, language_code: str
):
    context.chat_data[CONTEXT_LANGUAGE_KEY] = language_code


def validate_language_code(language_code: str):
    return language_code in settings.LANGUAGES_DICT


def normalize_language_code(language_code: str):
    language_code = language_code.lower()
    return language_code if validate_language_code(language_code) else None


async def safe_reply(
    update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, **kwargs
):
    """
    Safely reply to a message using the chat's current language.
    Accepts lazy strings.
    """
    message = update.effective_message
    if message:
        language_code = get_context_language(context)
        with override(language_code):
           reply_message = await message.reply_text(str(text).format(**kwargs))
        return reply_message