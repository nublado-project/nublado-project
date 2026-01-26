from telegram import Update
from telegram.ext import ContextTypes

from django_telegram.permissions import (
    group_only,
    private_only,
)
from django_telegram.handlers import BaseTelegramHandler


class StartHandler(BaseTelegramHandler):
    @private_only
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello from Nublado.")


class HelloHandler(BaseTelegramHandler):
    @group_only
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hello everybody.")
