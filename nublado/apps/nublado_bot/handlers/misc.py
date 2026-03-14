from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import gettext_lazy as _

from django_telegram.utils.helpers import safe_reply
from django_telegram.utils.jobs import delete_message_job
from django_telegram.utils.decorators import with_language
from ..bot_messages import BOT_MESSAGES


@with_language
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_chat = update.effective_chat
    tg_message = update.effective_message

    await context.bot.send_message(
        chat_id=tg_chat.id,
        text=str(BOT_MESSAGES["bot_start"]),
        reply_to_message_id=tg_message.message_id
    )

@with_language
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_chat = update.effective_chat
    command_message = update.effective_message

    hello_message = await context.bot.send_message(
        chat_id=tg_chat.id,
        text=str(BOT_MESSAGES["bot_hello"]),
        reply_to_message_id=command_message.message_id
    )

    context.job_queue.run_once(
        delete_message_job,
        10,
        data={
            "chat_id": tg_chat.id,
            "message_ids": [command_message.message_id, hello_message.message_id],
        }
    )