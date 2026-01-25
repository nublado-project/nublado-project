import logging

from telegram.ext import Application

from django.conf import settings

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

    return app
