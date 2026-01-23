from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...apps import DjangoTelegramConfig

# class Command(BaseCommand):
#     help = "Initialize and run Telegram bots."

#     def add_arguments(self, parser):
#         parser.add_argument('bot_ids', nargs='+', type=str)

#     def handle(self, *args, **options):
#         if options['bot_ids']:
#             for bot_id in options['bot_ids']:
#                 bot = DjangoTelegramConfig.bot_registry.get_bot(bot_id)
#                 if bot:
#                     bot.start_polling()
#                 else:
#                     error = f"Bot id {bot_id} doesn't exist or is improperly configured."
#                     raise CommandError(error)
#         return
