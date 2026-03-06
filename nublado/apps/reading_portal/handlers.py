from telegram import Update
from telegram.ext import ContextTypes

from django_telegram.models import TelegramChat
from django_telegram.utils.helpers import safe_reply

from .models import ReadingPortal

from reading_portal.services.portals import (
    NoDraftPortal,
    OpenPortalExists,
    open_next_draft_portal_service, 
    close_portal_service
)


async def open_portal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_chat = update.effective_chat

    try:
        await open_next_draft_portal_service(tg_chat, context.bot)
    except OpenPortalExists:
        await safe_reply(update, context, "A portal is aleady open.")
    except NoDraftPortal:
        await safe_reply(update, context, "No draft portal found.")


async def close_portal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_chat = update.effective_chat
    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)

    try:
        portal = await ReadingPortal.objects.aget_open(chat=chat)
        await close_portal_service(tg_chat, context.bot, portal)

    except ReadingPortal.DoesNotExist:
        error_msg = "There is no portal currently open."
        await safe_reply(update, context, error_msg)


# async def bind_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not update.message.reply_to_message:
#         error_msg = _("reading_portal.validation.reply_to_reading_text")
#         await safe_reply(update, context, error_msg)
#         return

#     reply_to_msg = update.message.reply_to_message

#     if not reply_to_msg.text:
#         error_msg = _("reading_portal.validation.reply_to_text_message")
#         await safe_reply(update, context, error_msg)
#         return

#     if not context.args:
#         # "Usage: /bind_reading <en|es>"
#         error_msg = _("reading_portal.validation.bing_reading_usage")
#         await safe_reply(update, context, error_msg)
#         return

#     language = context.args[0].lower()

#     if language not in ReadingPortal.REQUIRED_LANGUAGES:
#         error_msg = _("reading_portal.validation.invalid_language {language} {valid_languages}")
#         await safe_reply(
#             update,
#             context,
#             error_msg,
#             language=language,
#             valid_languages=ReadingPortal.REQUIRED_LANGUAGES
#         )
#         return

#     tg_chat = update.effective_chat

#     # ORM async
#     chat = TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)
#     portal, created = await ReadingPortal.objects.aget_or_create(
#         chat=chat,
#         portal_status=ReadingPortal.PortalStatus.DRAFT,
#         defaults={
#             "title": "New Reading Portal",
#             "opens_at": timezone.now(),
#             "closes_at": timezone.now() + timedelta(days=7),
#         }
#     )
#     reading = await PortalReading.objects.aupdate_or_create(
#         reading_portal=portal,
#         language=language,
#         defaults={
#             "message_id": reply_to_msg.message_id,
#             "message_text": reply_to_msg.text
#         }
#     )
#     confirmation_msg = _("reading_portal.bind_reading.success {language}")
#     await safe_reply(
#         update,
#         context,
#         confirmation_msg,
#         language=language.upper()
#     )
