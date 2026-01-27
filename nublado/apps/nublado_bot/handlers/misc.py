from telegram import Update
from telegram.ext import ContextTypes

from django.utils.translation import gettext as _

from django_telegram.utils import safe_reply
from ..bot_messages import BOT_MESSAGES


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_reply(update, _(BOT_MESSAGES["bot_start"]))



async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await safe_reply(update, _(BOT_MESSAGES["bot_hello"]))
