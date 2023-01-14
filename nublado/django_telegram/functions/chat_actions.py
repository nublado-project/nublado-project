from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction


def send_action(action):
    def decorator(func):
        @wraps(func)
        async def command_func(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            await context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id,
                action=action
            )
            return await func(update, context, *args, **kwargs)
        return command_func

    return decorator


send_typing_action = send_action(ChatAction.TYPING)
send_upload_photo_action = send_action(ChatAction.UPLOAD_PHOTO)
send_upload_video_action = send_action(ChatAction.UPLOAD_VIDEO)