from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update

from django.conf import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello from Nublado.")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello everybody except Christopher.")


def create_app() -> Application:
    # Create the application.
    app = Application.builder().token(
        settings.NUBLADO_BOT_TOKEN
    ).build()

    # Add the command handlers.
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))

    return app