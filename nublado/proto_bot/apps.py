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
        from .bot_commands.group_points import (
            add_points_handler, remove_points_handler
        )
        from .bot_commands.group_notes import (
            group_notes,
            save_group_note,
            remove_group_note,
            get_group_note_handler
        )
        from .bot_commands.misc import (
            start, echo, hello, roll,
            roll_sum, get_time, reverse_text
        )

        bot_registry = DjangoTelegramConfig.bot_registry
        bot = Bot(settings.PROTO_BOT_TOKEN)

        # Register handlers
        # misc
        bot.add_command_handler('start', start)
        bot.add_command_handler('reverse', reverse_text)
        bot.add_command_handler('echo', echo)
        bot.add_command_handler('hello', hello)
        bot.add_command_handler('roll', roll)
        bot.add_command_handler('roll_sum', roll_sum)
        bot.add_command_handler('get_time', get_time)
        # group_points
        bot.add_handler(add_points_handler, handler_group=2)
        bot.add_handler(remove_points_handler, handler_group=2)
        # notes
        bot.add_command_handler('group_notes', group_notes)
        bot.add_command_handler('save_group_note', save_group_note)
        bot.add_command_handler('remove_group_note', remove_group_note)
        bot.add_handler(get_group_note_handler, handler_group=2)
        # Add the bot to the registry.
        bot_registry.add_bot(ProtoBotConfig.bot_key, bot)

