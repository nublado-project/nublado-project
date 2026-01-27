from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import gettext as _

BOT_MESSAGES = {
    "bot_start": "bot.message.start",
    "bot_hello": "bot.message.hello"
}


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
