from telegram.ext import Application, CommandHandler

from django.conf import settings

async def start(update, context):
    await update.message.reply_text("Hello")

async def hello(update, context):
    await update.message.reply_text("Hello everybody.")

def get_application():
    app = Application.builder().token(
        settings.DJANGO_TELEGRAM_BOT_TOKEN
    ).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))
    return app