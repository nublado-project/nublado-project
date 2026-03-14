from telegram.ext import ContextTypes


async def delete_message_job(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.data["chat_id"]

    for message_id in job.data["message_ids"]:
        try:
            await context.bot.delete_message(chat_id, message_id)
        except Exception:
            pass