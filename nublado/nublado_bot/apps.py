import logging

from django.conf import settings
from django.apps import AppConfig

from django_telegram.apps import DjangoTelegramConfig
from django_telegram.bot import Bot

logger = logging.getLogger('django')


class NubladoBotConfig(AppConfig):
    name = "nublado_bot"
    bot_key = settings.NUBLADO_BOT_TOKEN
    bot_name = settings.NUBLADO_BOT

    def ready(self):
        from .bot_commands.group_points import (
            add_point_handler,
            add_points_handler,
            remove_point_handler,
            remove_points_handler
        )
        from .bot_commands.group_notes import (
            group_notes,
            save_group_note,
            remove_group_note,
            get_group_note_handler
        )
        from .bot_commands.group_admin import(
            member_join_handler,
            member_exit_handler,
            welcome_button_handler,
            set_bot_language
        )
        from .bot_commands.misc import (
            start, get_time, reverse_text,
            echo, hello, roll, roll_sum
        )

        bot_registry = DjangoTelegramConfig.bot_registry
        bot = Bot(settings.NUBLADO_BOT_TOKEN, name=settings.NUBLADO_BOT)

        # Register handlers
        
        # group_admin
        bot.add_command_handler('set_bot_language', set_bot_language)
        bot.add_handler(member_join_handler)
        bot.add_handler(member_exit_handler)
        bot.add_handler(welcome_button_handler)
        # misc
        bot.add_command_handler('start', start)
        bot.add_command_handler('reverse', reverse_text)
        bot.add_command_handler('echo', echo)
        bot.add_command_handler('hello', hello)
        bot.add_command_handler('roll', roll)
        bot.add_command_handler('roll_sum', roll_sum)
        bot.add_command_handler('get_time', get_time)
        # group_points
        bot.add_handler(add_point_handler)
        bot.add_handler(add_points_handler)
        bot.add_handler(remove_point_handler)
        bot.add_handler(remove_points_handler)
        # notes
        bot.add_command_handler('group_notes', group_notes)
        bot.add_command_handler('save_group_note', save_group_note)
        bot.add_command_handler('remove_group_note', remove_group_note)
        bot.add_handler(get_group_note_handler)
        # Add the bot to the registry.
        bot_registry.add_bot(NubladoBotConfig.bot_name, bot)
