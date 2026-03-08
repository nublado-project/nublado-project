from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from django_telegram.models import TelegramChat, TelegramGroupMember

from ..models import ReadingPortal, PortalReading, ReadingSubmission
from ..exceptions import NoOpenPortal, NoReplyToAudio, NoAudioReplyToText, NoReplyToReading


async def submit_reading_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Submit a reading to the Reading Portal.
    """
    tg_chat = update.effective_chat
    tg_message = update.effective_message
    tg_user = update.effective_user
    bot = context.bot

    # Must be a voice message
    if not tg_message or not tg_message.voice:
        return None

    # Must reply to a reading
    text_message = tg_message.reply_to_message
    if not text_message or not text_message.text:
        return None

    if text_message.from_user.id != context.bot.id:
        return None

    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)

    try:
        portal = await ReadingPortal.objects.aget_open(chat=chat)
    except ReadingPortal.DoesNotExist:
        raise NoOpenPortal()

    try:
        reading = await PortalReading.objects.select_related("reading_portal").aget(
            reading_portal=portal, 
            message_id=text_message.message_id,
        )
    except PortalReading.DoesNotExist:
        raise NoReplyToReading()

    tg_member = await bot.get_chat_member(tg_chat.id, tg_user.id)
    member = await TelegramGroupMember.objects.aget_or_create_from_chat_member(
        tg_member, tg_chat
    )

    # Delete old reading submission if this is a resubmission.
    old_submission = await ReadingSubmission.objects.filter(
        portal_reading=reading,
        member=member,
        reading_status=ReadingSubmission.ReadingStatus.PENDING,
    ).afirst()

    if old_submission:
        # Delete the old voice message
        try:
            await bot.delete_message(
                chat_id=tg_chat.id,
                message_id=old_submission.message_id
            )
        except BadRequest:
            # Message may already be deleted.
            pass

        # Delete the old reading submissions bot reply if it exists.
        if old_submission.reply_message_id:
            try:
                await bot.delete_message(
                    chat_id=tg_chat.id,
                    message_id=old_submission.reply_message_id
                )
            except BadRequest:
                pass

        # Hard delete the old submission from the db.
        await old_submission.adelete()

    # Create a new reading submission.
    reading_submission = await ReadingSubmission.objects.acreate(
        portal_reading=reading,
        member=member,
        message_id=tg_message.message_id,
        reading_status=ReadingSubmission.ReadingStatus.PENDING,
    )

    return reading_submission

# async def submit_reading_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     tg_chat = update.effective_chat
#     tg_message = update.effective_message
#     bot = context.bot

#     chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)

#     # Make sure there is an open portal to submit readings to.
#     try:
#         portal = await ReadingPortal.objects.aget_open(chat=chat)
#     except ReadingPortal.DoesNotExist:
#         raise NoOpenPortal()

#     # Make sure /submit_reading (or whatever the command) is a reply to voice message.
#     voice_message = tg_message.reply_to_message if tg_message else None

#     if not voice_message or not voice_message.voice:
#         raise NoReplyToAudio()

#     # Can't do reply_to_message.reply_to_message, so fetch
#     # the voice message from chat, then check if it's a reply.abs

#     voice_message = await bot.get_message(chat_id=tg_chat.id, message_id=voice_message.message_id)

#     print(voice_message)

#     # Is the voice message a reply to a text message?
#     if not text_message or not text_message.text:
#         raise NoAudioReplyToText()

#     # Is the text message one of the portal readings?
#     try:
#         reading = await PortalReading.objects.select_related("reading_portal").aget(
#             reading_portal=portal, 
#             message_id=text_message.message_id,
#         )
#     except PortalReading.DoesNotExist:
#         raise NoReplyToReading()

#     # get TelegramGroupMember
#     tg_member = await bot.get_chat_member(tg_chat.id, update.effective_user.id)
#     member = await TelegramGroupMember.objects.aget_or_create_from_chat_member(
#         tg_member, tg_chat
#     )
#     reading_submission = await ReadingSubmission.objects.acreate(
#         portal_reading=reading,
#         member=member,
#         message_id=voice_message.message_id,
#         reading_status=ReadingSubmission.ReadingStatus.PENDING,
#     )

#     return reading_submission