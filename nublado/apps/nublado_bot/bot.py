from telegram.ext import Application, CommandHandler

from django.conf import settings

from .handlers import start, hello


def create_app() -> Application:
    # Create the application.
    app = Application.builder().token(
        settings.NUBLADO_BOT_TOKEN
    ).build()

    # Add the command handlers.
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))

    return app