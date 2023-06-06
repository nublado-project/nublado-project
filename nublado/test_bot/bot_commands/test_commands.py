import logging

from telegram import Update
from telegram.ext import ContextTypes

from django.conf import settings
from django.utils.translation import gettext as _

logger = logging.getLogger('django')

BOT_MESSAGES = {
    "testing": _("testing testing")
}

async def test_bot_output(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a dummy message for testing."""
    bot_message = _(BOT_MESSAGES['testing'])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot_message
    )
