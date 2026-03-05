import logging

from telegram.ext import CommandHandler, MessageHandler

from django.apps import AppConfig
from django.conf import settings

from django_telegram.bot_registry import registry

from .bot import create_app

logger = logging.getLogger("django")
BOT_NAME = settings.NUBLADO_BOT


class NubladoBotConfig(AppConfig):
    name = "nublado_bot"

    def ready(self):
        from django_telegram.policies import GroupOnly, PrivateOnly, with_policies
        from .handlers.group_points import give_points, POINT_FILTER
        from .handlers.misc import start, hello
        from .handlers.group_settings import set_bot_language
        from django_telegram.utils.database import resolve_chat_language
        from django_telegram.handlers import LanguageHandler
        from django_telegram.constants import MIDDLEWARE_GROUP, HANDLER_GROUP

        from reading_portal.handlers import bind_reading

        app = create_app()
        app.bot_data["language_resolver"] = resolve_chat_language
        registry.register(BOT_NAME, app)

        # Middleware
        app.add_handler(LanguageHandler(), group=MIDDLEWARE_GROUP)

        # Command handlers.
        app.add_handler(
            CommandHandler(
                "start",
                with_policies(PrivateOnly())(start),
            ),
            group=HANDLER_GROUP,
        )

        app.add_handler(
            CommandHandler(
                "hello",
                with_policies(GroupOnly())(hello),
            ),
            group=HANDLER_GROUP,
        )

        app.add_handler(
            CommandHandler(
                "set_bot_language",
                with_policies(GroupOnly())(set_bot_language),
            ),
            group=HANDLER_GROUP,
        )

        # Reading Portal
        app.add_handler(
            CommandHandler(
                "bind_reading",
                with_policies(GroupOnly())(bind_reading),
            ),
            group=HANDLER_GROUP,
        )

        # Message handlers.
        group_give_points = with_policies(GroupOnly())(give_points)
        app.add_handler(
            MessageHandler(
                POINT_FILTER,
                group_give_points,
            ),
            group=HANDLER_GROUP,
        )
