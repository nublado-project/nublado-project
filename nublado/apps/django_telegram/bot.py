from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

from django.conf import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello everybody!")


def get_application() -> Application:
    application = (
        Application.builder().token(settings.DJANGO_TELEGRAM_BOT_TOKEN).build()
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hello", hello))
    return application
