from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import gettext_lazy as _

from django_telegram.permissions import (
    group_only,
    private_only,
)
from django_telegram.handlers import BaseTelegramHandler

BOT_MESSAGES = {
    "bot_start": _(
        "bot.message.start"
    ),
    "bot_hello": _("bot.message.hello")
}

class StartHandler(BaseTelegramHandler):
    @private_only
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(BOT_MESSAGES["bot_start"])


class HelloHandler(BaseTelegramHandler):
    @group_only
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(BOT_MESSAGES["bot_hello"])
