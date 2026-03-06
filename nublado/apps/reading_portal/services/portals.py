from telegram import Bot, Chat
from telegram.error import BadRequest

from django_telegram.models import TelegramChat

from reading_portal.models import ReadingPortal

from .formatting import format_portal_intro, format_reading, format_portal_closed


class NoDraftPortal(Exception):
    pass


class OpenPortalExists(Exception):
    pass


async def open_next_draft_portal_service(tg_chat: Chat, bot: Bot, notify: bool = False):
    """
    Open the next draft portal for the given Telegram chat.
    """

    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)

    # Check if an open portal already exists in the group.
    existing_open = await ReadingPortal.objects.filter(
        chat=chat, portal_status=ReadingPortal.PortalStatus.OPEN
    ).aexists()

    if existing_open:
        raise OpenPortalExists()

    portal = await ReadingPortal.objects.anext_draft(chat=chat)

    if not portal:
        raise NoDraftPortal()

    intro_text = format_portal_intro(portal)

    intro_msg = await bot.send_message(
        chat_id=tg_chat.id,
        text=intro_text,
        parse_mode="HTML",
    )

    async for reading in portal.portal_readings.all():

        language_label = reading.language.upper()
        header = f"🌧 <b>Reading: {language_label}</b>"
        reading_text = f"{header}\n\n{reading.message_text}"

        reading_msg = await bot.send_message(
            chat_id=tg_chat.id,
            text=reading_text,
            parse_mode="HTML",
        )

        reading.message_id = reading_msg.message_id
        await reading.asave(update_fields=["message_id"])

    await bot.pin_chat_message(
        chat_id=tg_chat.id,
        message_id=intro_msg.message_id,
        disable_notification=not notify,
    )

    portal.pinned_message_id = intro_msg.message_id
    portal.portal_status = ReadingPortal.PortalStatus.OPEN

    await portal.asave(update_fields=["portal_status", "pinned_message_id"])

    return portal


async def close_portal_service(tg_chat: Chat, bot: Bot, portal: ReadingPortal, notify: bool = False):

    # Unpin intro message
    if portal.pinned_message_id:
        try:
            await bot.unpin_chat_message(
                chat_id=tg_chat.id,
                message_id=portal.pinned_message_id,
            )
        except BadRequest:
            pass

    closed_msg = await bot.send_message(
        chat_id=tg_chat.id,
        text=format_portal_closed(),
        parse_mode="HTML",
    )

    await bot.pin_chat_message(
        chat_id=tg_chat.id,
        message_id=closed_msg.message_id,
        disable_notification=not notify,
    )

    portal.portal_status = portal.PortalStatus.CLOSED
    portal.pinned_message_id = None

    await portal.asave(update_fields=["portal_status", "pinned_message_id"])
