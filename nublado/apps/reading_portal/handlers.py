from telegram import Update, ReactionTypeEmoji
from telegram.ext import ContextTypes

from django_telegram.utils.helpers import safe_reply, user_link

from .exceptions import (
    NoDraftPortal,
    NoOpenPortal,
    OpenPortalExists,
    NoReplyToAudio,
    NoAudioReplyToText,
    NoReplyToReading,
    EmptyPortal,
)
from .services.portals import (
    open_next_draft_portal_service,
    close_open_portal_service,
)
from .services.reading_submissions import (
    submit_reading_service,
)


async def open_portal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await open_next_draft_portal_service(update, context)
    except OpenPortalExists:
        await safe_reply(update, context, "A portal is aleady open.")
        return
    except NoDraftPortal:
        await safe_reply(update, context, "No draft portal found.")
        return
    except EmptyPortal:
        await safe_reply(update, context, "A Reading Portal can't be empty.")
        return


async def close_portal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await close_open_portal_service(update, context)
    except NoOpenPortal:
        error_message = "There is no portal currently open."
        await safe_reply(update, context, error_message)
        return

async def handle_voice_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        reading_submission = await submit_reading_service(update, context)
    except NoOpenPortal:
        return
    except NoReplyToReading:
        return

    if reading_submission:
        tg_user = update.effective_user
        portal_reading = reading_submission.portal_reading
        message = f"#pending_{portal_reading.language} : {user_link(tg_user)}"

        reply_message = await safe_reply(update, context, message)

        await context.bot.set_message_reaction(
            chat_id=update.effective_chat.id,
            message_id=reading_submission.message_id,
            reaction=[ReactionTypeEmoji("⚡️")]
        )

        reading_submission.reply_message_id = reply_message.message_id
        await reading_submission.asave(update_fields=["reply_message_id"])

# async def submit_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         reading_submission = await submit_reading_service(update, context)
#     except NoOpenPortal:
#         error_message = "There is no portal currently open."
#         await safe_reply(update, context, error_message)
#         return
#     except NoReplyToAudio:
#         error_message = "The command must be a reply to a voice message."
#         await safe_reply(update, context, error_message)
#         return
#     except NoAudioReplyToText:
#         error_message = "The reading voice message must be a reply to a text message."
#         await safe_reply(update, context, error_message)
#         return
#     except NoReplyToReading:
#         error_message = "The reading voice message must be a reply to a portal reading text."
#         await safe_reply(update, context, error_message)
#         return

#     await safe_reply(update, context, "Thank you for submitting your reading.")


# async def bind_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if not update.message.reply_to_message:
#         error_message = _("reading_portal.validation.reply_to_reading_text")
#         await safe_reply(update, context, error_message)
#         return

#     reply_to_message = update.message.reply_to_message

#     if not reply_to_message.text:
#         error_message = _("reading_portal.validation.reply_to_text_message")
#         await safe_reply(update, context, error_message)
#         return

#     if not context.args:
#         # "Usage: /bind_reading <en|es>"
#         error_message = _("reading_portal.validation.bing_reading_usage")
#         await safe_reply(update, context, error_message)
#         return

#     language = context.args[0].lower()

#     if language not in ReadingPortal.REQUIRED_LANGUAGES:
#         error_message = _("reading_portal.validation.invalid_language {language} {valid_languages}")
#         await safe_reply(
#             update,
#             context,
#             error_message,
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
#             "message_id": reply_to_message.message_id,
#             "message_text": reply_to_message.text
#         }
#     )
#     confirmation_message = _("reading_portal.bind_reading.success {language}")
#     await safe_reply(
#         update,
#         context,
#         confirmation_message,
#         language=language.upper()
#     )
