import asyncio

from django.apps import AppConfig
from .bot_application import application
#from .bot import Bot


# class BotRegistry:
#     def __init__(self):
#         self.bots = {}

#     def add_bot(self, key: str, bot: Bot) -> None:
#         self.bots[key] = bot

#     def get_bot(self, key: str):
#         return self.bots.get(key, None)


class DjangoTelegramConfig(AppConfig):
    name = "django_telegram"

    # def ready(self):
    #     loop = asyncio.get_event_loop()
    #     loop.create_task(application.initialize())