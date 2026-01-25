from telegram import Update
from telegram.ext import ContextTypes

from django_telegram.permissions import (
    group_only,
    private_only,
)


@private_only
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello from Nublado.")


@group_only
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello everybody."
    )
