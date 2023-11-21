import logging

from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import (
    ContextTypes, MessageHandler, filters
)
from telegram.error import TelegramError

from django.utils.translation import gettext as _

from django_telegram.functions.functions import parse_command_last_arg_text
from ..models import GroupNote
from ..bot_messages import BOT_MESSAGES

logger = logging.getLogger('django')

TAG_CHAR = '#'
GET_GROUP_NOTE_REGEX = '^[' + TAG_CHAR + '][a-zA-Z0-9_-]+$'


async def group_notes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None
) -> None:
    if group_id is not None:
        group_notes = GroupNote.objects.filter(group_id=group_id).order_by('note_tag')

        if await sync_to_async(group_notes.count)():
            group_notes_list = [f"*- {note.note_tag}*" async for note in group_notes]
            bot_message = _(BOT_MESSAGES['notes_list']).format(
                notes="\n".join(group_notes_list)
            )
        else:
            bot_message = _(BOT_MESSAGES['no_notes'])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=bot_message
    )


async def save_group_note(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None,
    repo_id: int = None
) -> None:
    if group_id is not None and repo_id is not None:
        # Is at least a tag provided?
        if context.args:
            note_tag = context.args[0]
            if update.message.reply_to_message:
                note_message_id = update.message.reply_to_message.message_id
                try:
                    copied_message = await context.bot.copy_message(
                        chat_id=repo_id,
                        from_chat_id=update.effective_chat.id,
                        message_id=note_message_id
                    )
                    obj, created = await GroupNote.objects.aupdate_or_create(
                        note_tag=note_tag,
                        group_id=group_id,
                        defaults={
                            'message_id': copied_message.message_id
                        }
                    )
                    bot_message = _(BOT_MESSAGES['note_saved']).format(
                        note_tag=note_tag
                    )
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        reply_to_message_id=update.message.message_id,
                        text=bot_message
                    )
                except Exception as e:
                    logger.error(e)
            else:
                if len(context.args) > 1:
                    content = parse_command_last_arg_text(
                        update.effective_message,
                        maxsplit=2
                    )
                    try:
                        message = await context.bot.send_message(
                            chat_id=repo_id,
                            text=content
                        )
                        obj, created = await GroupNote.objects.aupdate_or_create(
                            note_tag=note_tag,
                            group_id=group_id,
                            defaults={
                                'message_id': message.message_id
                            }
                        )
                        bot_message = _(BOT_MESSAGES['note_saved']).format(
                            note_tag=note_tag
                        )
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            reply_to_message_id=update.message.message_id,
                            text=bot_message
                        )
                    except Exception as e:
                        logger.error(e)
                else:
                    bot_message = _(BOT_MESSAGES['note_no_content'])
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        reply_to_message_id=update.message.message_id,
                        text=bot_message
                    )
        else:
            bot_message = _(BOT_MESSAGES['note_no_tag'])
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.message_id,
                text=bot_message
            )


async def remove_group_note(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None,
    repo_id: int = None
) -> None:
    """Removes a group note specified by a tag argument."""
    if group_id is not None and repo_id is not None:
        if context.args:
            note_tag = context.args[0]
            num_removed, removed_dict = await GroupNote.objects.filter(
                note_tag=note_tag,
                group_id=group_id
            ).adelete()
            if num_removed > 0:
                # Pending: Delete message from repo, but what about the 48-hour limitation?

                bot_message = _(BOT_MESSAGES['note_removed']).format(
                    note_tag=note_tag
                )
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    reply_to_message_id=update.message.message_id,
                    text=bot_message
                )
            else:
                bot_message = _(BOT_MESSAGES['note_no_exist']).format(
                    note_tag=note_tag
                )
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    reply_to_message_id=update.message.message_id,
                    text=bot_message
                )
        else:
            bot_message = _(BOT_MESSAGES['note_no_tag'])
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.message_id,
                text=bot_message
            )


async def get_group_note(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None,
    repo_id: int = None,
    tag_char: str = TAG_CHAR
) -> None:
    """Retrieves a group note specified by a tag argument."""
    if group_id is not None and repo_id is not None:
        message = update.message.text
        if message.startswith(tag_char):
            note_tag = message.lstrip(tag_char)
            try:
                group_note = await GroupNote.objects.aget(
                    note_tag=note_tag,
                    group_id=group_id
                )
                try:
                    if update.message.reply_to_message:
                        note_message_id = update.message.reply_to_message.message_id
                    else
                        note_message_id = update.message.message_id

                    copied_message = await context.bot.copy_message(
                        chat_id=update.effective_chat.id,
                        from_chat_id=repo_id,
                        message_id=group_note.message_id,
                        reply_to_message_id=note_message_id
                    )
                except:
                    bot_message = _(BOT_MESSAGES['note_not_in_repo']).format(
                        note_tag=note_tag
                    )
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        reply_to_message_id=update.message.message_id,
                        text=bot_message
                    )            
            except GroupNote.DoesNotExist:
                pass


# Handlers to listen for triggers to retrieve notes.
get_group_note_handler = MessageHandler(
    filters.Regex(GET_GROUP_NOTE_REGEX),
    get_group_note
)
