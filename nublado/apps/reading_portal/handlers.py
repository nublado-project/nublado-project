from collections import defaultdict

from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from django.utils.translation import gettext_lazy as _

from django_telegram.utils.helpers import safe_reply, user_display_name, message_link, delete_command
from django_telegram.utils.decorators import with_language
from django_telegram.utils.jobs import delete_message_job 

from .exceptions import ReadingPortalError, NoPendingReading
from .services.portals import (
    open_portal_service,
    close_open_portal_service,
    list_draft_portals_service,
)
from .services.reading_submissions import (
    submit_reading_service,
    review_reading_service,
    get_pending_readings_service,
)


async def open_portal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    slug = None

    if context.args:
        slug = context.args[0]

    try:
        await open_portal_service(update, context, slug, True)
    except ReadingPortalError as e:
        await safe_reply(update, context, str(e))
        return

    # Delete the lingering command in the chat.
    await delete_command(update)


async def open_portal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # <-- stops the “freezing” spinner
    data = query.data

    if data.startswith("open_portal:"):
        slug = data.split(":", 1)[1]

        try:
            await open_portal_service(update, context, slug=slug)
            # Remove the buttons after opening
            await query.message.delete()
        except ReadingPortalError as e:
            # Reply in chat if something goes wrong
            await query.message.reply_text(str(e))


async def close_portal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await close_open_portal_service(update, context)
    except ReadingPortalError as e:
        await safe_reply(update, context, str(e))
        return

    # Delete the lingering command in the chat.
    await delete_command(update)


async def list_draft_portals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    portals = await list_draft_portals_service(update, context)

    if not await portals.aexists():
        await safe_reply(update, context, _("reading_portal.error.no_draft_portal"))
        return

    message = "READING PORTALS:\n"
    buttons = []

    async for portal in portals:
        buttons.append([
            InlineKeyboardButton(
                f"{portal.title}",
                callback_data=f"open_portal:{portal.slug}",
            )
        ])

    keyboard = InlineKeyboardMarkup(buttons)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=keyboard,
    )

    # Delete the lingering command in the chat.
    await delete_command(update)


async def handle_voice_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        reading_submission = await submit_reading_service(update, context)
    except ReadingPortalError as e:
        await safe_reply(update, context, str(e))
        return

    if reading_submission:
        tg_user = update.effective_user
        portal_reading = reading_submission.portal_reading
        message = f"#pending_{portal_reading.language} : {user_display_name(tg_user)}"

        reply_message = await safe_reply(update, context, message)

        await context.bot.set_message_reaction(
            chat_id=update.effective_chat.id,
            message_id=reading_submission.message_id,
            reaction=[ReactionTypeEmoji("⚡️")]
        )

        reading_submission.reply_message_id = reply_message.message_id
        await reading_submission.asave(update_fields=["reply_message_id"])

@with_language
async def pending_readings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    init_message = update.effective_message
    tg_chat = update.effective_chat

    try:
        pending_readings = await get_pending_readings_service(update, context)
    except ReadingPortalError as e:
        await safe_reply(update, context, str(e))
        return

    if not await pending_readings.aexists():
        await safe_reply(update, context, _("reading_portal.error.no_pending_readings"))
        return

    readings_by_member = defaultdict(list)

    async for pending_reading in pending_readings:
        readings_by_member[pending_reading.member].append(pending_reading)

    readings_list = ["Pending Readings:"]

    for member, readings in readings_by_member.items():
        language_links = []

        for reading in readings:
            link = message_link(tg_chat.id, reading.message_id)
            language = reading.portal_reading.language.upper()
            language_links.append(f'<a href="{link}">{language}</a>')

        readings_list.append(f"{member.mention_html}: {', '.join(language_links)}")

    readings_message = await context.bot.send_message(
        chat_id=tg_chat.id,
        text="\n".join(readings_list),
    )

    context.job_queue.run_once(
        delete_message_job,
        30,
        data={
            "chat_id": tg_chat.id,
            "message_ids": [init_message.message_id, readings_message.message_id],
        }
    )


async def review_reading(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        reading_submission = await review_reading_service(update, context)
    except NoPendingReading:
        await safe_reply(update, context, _("reading_portal.error.review_no_pending_reading"))
        return
    except ReadingPortalError as e:
        await safe_reply(update, context, str(e))
        return

    if reading_submission:  
        tg_user = update.effective_user
        tg_chat = update.effective_chat
        portal_reading = reading_submission.portal_reading

        await context.bot.set_message_reaction(
            chat_id=tg_chat.id,
            message_id=reading_submission.message_id,
            reaction=[ReactionTypeEmoji("💯")]
        )
       
        message = f"✨ Reviewed by {user_display_name(tg_user)}."

        await context.bot.send_message(
            chat_id=tg_chat.id,
            text=message,
            reply_to_message_id=reading_submission.message_id
        )

        if reading_submission.reply_message_id:
            try:
                await context.bot.delete_message(
                    chat_id=tg_chat.id,
                    message_id=reading_submission.reply_message_id
                )
            except BadRequest:
                pass

    # Delete the lingering command in the chat.
    await delete_command(update)
