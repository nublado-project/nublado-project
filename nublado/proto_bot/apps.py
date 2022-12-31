import logging

from django.conf import settings
from django.apps import AppConfig

from django_telegram.apps import DjangoTelegramConfig
from django_telegram.bot import Bot

logger = logging.getLogger('django')


class ProtoBotConfig(AppConfig):
    name = 'proto_bot'
    bot_key = settings.PROTO_BOT_TOKEN

    def ready(self):
        from .bot_commands.misc import (
            start, echo, roll,
            roll_sum, get_time, reverse_text
        )

        bot_registry = DjangoTelegramConfig.bot_registry
        bot = Bot(settings.PROTO_BOT_TOKEN)

        # Register handlers
        # misc
        bot.add_command_handler('start', start)
        bot.add_command_handler('echo', echo)
        bot.add_command_handler('roll', roll)
        bot.add_command_handler('roll_sum', roll_sum)
        bot.add_command_handler('get_time', get_time)
        bot.add_command_handler('reverse', reverse_text)

        # Add the bot to the registry.
        bot_registry.add_bot(ProtoBotConfig.bot_key, bot)

