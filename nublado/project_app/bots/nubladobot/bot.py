import logging

from django_telegram.bot import Bot
from .bot_commands.group_points import (
    add_point_handler, add_points_handler, remove_points_handler
)
from .bot_commands.group_notes import (
    group_notes,
    save_group_note,
    remove_group_note,
    get_group_note_handler
)
from .bot_commands.group_admin import(
    # update_group_admins,
    # get_non_members,
    member_join_handler,
    member_exit_handler,
    welcome_button_handler,
    set_bot_language
)
from .bot_commands.misc import (
    start, get_time, reverse_text,
    echo, hello, roll, roll_sum
)

logger = logging.getLogger('django')


class NubladoBot(Bot):
    def setup_handlers(self):
        logger.info(f"Registering handlers for {self.name}.")
        # Register handlers
        # group_admin
        # self.add_command_handler('update_group_admins', update_group_admins)
        # self.add_command_handler('get_non_members', get_non_members)
        self.add_command_handler('set_bot_language', set_bot_language)
        self.add_handler(member_join_handler, handler_group=2)
        self.add_handler(member_exit_handler, handler_group=2)
        self.add_handler(welcome_button_handler, handler_group=2)
        # misc
        self.add_command_handler('start', start)
        self.add_command_handler('reverse', reverse_text)
        self.add_command_handler('echo', echo)
        self.add_command_handler('hello', hello)
        self.add_command_handler('roll', roll)
        self.add_command_handler('roll_sum', roll_sum)
        self.add_command_handler('get_time', get_time)
        # group_points
        self.add_handler(add_point_handler, handler_group=2)
        self.add_handler(add_points_handler, handler_group=2)
        self.add_handler(remove_points_handler, handler_group=2)
        # notes
        self.add_command_handler('group_notes', group_notes)
        self.add_command_handler('save_group_note', save_group_note)
        self.add_command_handler('remove_group_note', remove_group_note)
        self.add_handler(get_group_note_handler, handler_group=2)