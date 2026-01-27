from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import gettext as _

from ..bot_messages import BOT_MESSAGES


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_message = update.effective_message
    if not tg_message:
        return
    await tg_message.reply_text(_(BOT_MESSAGES["bot_start"]))



async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_message = update.effective_message
    if not tg_message:
        return
    await tg_message.reply_text(_(BOT_MESSAGES["bot_hello"]))
