from asgiref.sync import sync_to_async
from datetime import timedelta

from telegram import Update
from telegram.ext import ContextTypes

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_telegram.models import TelegramChat
from django_telegram.utils.helpers import safe_reply

from .models import ReadingPortal, PortalReading


async def bind_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        error_msg = _("reading_portal.validation.reply_to_reading_text")
        await safe_reply(update, context, error_msg)
        return

    reply_to_msg = update.message.reply_to_message

    if not reply_to_msg.text:
        error_msg = _("reading_portal.validation.reply_to_text_message")
        await safe_reply(update, context, error_msg)
        return

    if not context.args:
        # "Usage: /bind_reading <en|es>"
        error_msg = _("reading_portal.validation.bing_reading_usage")
        await safe_reply(update, context, error_msg)
        return

    language = context.args[0].lower()

    if language not in ReadingPortal.REQUIRED_LANGUAGES:
        error_msg = _("reading_portal.validation.invalid_language {language} {valid_languages}")
        await safe_reply(
            update,
            context,
            error_msg,
            language=language,
            valid_languages=ReadingPortal.REQUIRED_LANGUAGES
        )
        return

    tg_chat = update.effective_chat

    # ORM async
    chat = TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)
    portal, created = await ReadingPortal.objects.aget_or_create(
        chat=chat,
        portal_status=ReadingPortal.PortalStatus.DRAFT,
        defaults={
            "title": "New Reading Portal",
            "opens_at": timezone.now(),
            "closes_at": timezone.now() + timedelta(days=7),
        }
    )
    reading = await PortalReading.objects.aupdate_or_create(
        reading_portal=portal,
        language=language,
        defaults={
            "message_id": reply_to_msg.message_id,
            "message_text": reply_to_msg.text
        }
    )
    confirmation_msg = _("reading_portal.bind_reading.success {language}")
    await safe_reply(
        update,
        context,
        confirmation_msg,
        language=language.upper()
    )


async def open_portal(updat: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_chat = update.effective_chat
    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)

    try:
        portal = await ReadingPortal.objects.aget_draft(chat=chat)
    except ReadingPortal.DoesNotExist:
        error_msg = _("reading_portal.validation.no_draft_portal")
        await safe_reply(update, context, error_msg)
        return

    readings = portal.portal_readings.all()

    for reading in readings:
        if reading.message_id:
            continue

        sent = await context.bot.send_message(
            chat_id=portal.chat.telegram_id,
            text=reading.message_text
        )

        reading.message_id = sent.message_id
        await reading.asave(update_fields=["message_id"])

    portal.portal_status = ReadingPortal.PortalStatus.OPEN
    await portal.asave(update_fields=["portal_status"])