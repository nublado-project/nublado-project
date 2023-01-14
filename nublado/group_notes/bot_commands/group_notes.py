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
            message = _("*Group notes*\n{}").format(
                "\n".join(group_notes_list)
            )
        else:
            message = _("There are currently no group notes.")

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


async def save_group_note(
    update: Update, 
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None,
    repo_id: int = None
) -> None:
    if group_id is not None and repo_id is not None:
        if context.args:
            note_tag = context.args[0]
            saved_message = _("Group note *{note_tag}* has been saved.").format(
                note_tag=note_tag
            )
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
                            'message_id': copied_message.message_id,
                            'content': None
                        }
                    )
                    if obj:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            reply_to_message_id=update.message.message_id,
                            text=saved_message
                        )
                except TelegramError as e:
                    logger.info(e)
            else:
                if len(context.args) > 1:
                    content = parse_command_last_arg_text(
                        update.effective_message,
                        maxsplit=2
                    )
                    if content:
                        obj, created = await GroupNote.objects.aupdate_or_create(
                            note_tag=note_tag,
                            group_id=group_id,
                            defaults={
                                'message_id': None,
                                'content': content
                            }
                        )
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            reply_to_message_id=update.message.message_id,
                            text=saved_message
                        )
                    else:
                        message = _("A group note needs content.")
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            reply_to_message_id=update.message.message_id,
                            text=message
                        )
                else:
                    message = _("A group note needs content.")
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        reply_to_message_id=update.message.message_id,
                        text=message
                    )
        else:
            message = _("A group note must have a tag.")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.message_id,
                text=message
            )


async def remove_group_note(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    group_id: int = None
) -> None:
    """Removes a group note specified by a tag argument."""
    if group_id is not None:
        if context.args:
            note_tag = context.args[0]
            num_removed, removed_dict = await GroupNote.objects.filter(
                note_tag=note_tag,
                group_id=group_id
            ).adelete()
            if num_removed > 0:
                removed_message = _("The group note *{note_tag}* has been removed.").format(
                    note_tag=note_tag
                )
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    reply_to_message_id=update.message.message_id,
                    text=removed_message
                )
            else:
                not_found_message = _("The group note *{note_tag}* doesn't exist.").format(
                    note_tag=note_tag
                )
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    reply_to_message_id=update.message.message_id,
                    text=not_found_message
                )
        else:
            message = _("A group note must have a tag.")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.message.message_id,
                text=message
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
                if group_note.content:
                    try:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            reply_to_message_id=update.message.message_id,
                            text=group_note.content
                        )
                    except TelegramError as e:
                        logger.info(e)
                elif group_note.message_id:
                    try:
                        # context.bot.forward_message(
                        #     chat_id=update.effective_chat.id,
                        #     from_chat_id=REPO_ID,
                        #     message_id=group_note.message_id
                        # )
                        copied_message = await context.bot.copy_message(
                            chat_id=update.effective_chat.id,
                            from_chat_id=repo_id,
                            message_id=group_note.message_id,
                            reply_to_message_id=update.message.message_id
                        )
                    except:
                        not_found_message = _(
                            "The content for the group note *{note_tag}* was not found in the group repo."
                        ).format(
                            note_tag=note_tag
                        )
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            reply_to_message_id=update.message.message_id,
                            text=not_found_message
                        )            
                else:
                    pass
            except GroupNote.DoesNotExist:
                pass

# Handlers to listen for triggers to retrieve notes.
get_group_note_handler = MessageHandler(
    filters.Regex(GET_GROUP_NOTE_REGEX),
    get_group_note
)
