from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import gettext as _

from django_telegram.policies import GroupOnly, PrivateOnly
from django_telegram.handlers import BaseTelegramHandler

BOT_MESSAGES = {
    "bot_start": "bot.message.start",
    "bot_hello": "bot.message.hello"
}

class StartHandler(BaseTelegramHandler):
    policies = [PrivateOnly()]
    
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(_(BOT_MESSAGES["bot_start"]))


class HelloHandler(BaseTelegramHandler):
    policies = [GroupOnly()]

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(_(BOT_MESSAGES["bot_hello"]))
