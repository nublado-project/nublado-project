import logging

from telegram.ext import Application, CommandHandler

from django.conf import settings

from .handlers import start, hello

logger = logging.getLogger("django")


async def post_init(application: Application):
    logger.info(f"Bot {settings.NUBLADO_BOT} is running.")


def create_app() -> Application:
    # Create the application.
    app = (
        Application.builder()
        .token(settings.NUBLADO_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Add the command handlers.
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hello", hello))

    return app
