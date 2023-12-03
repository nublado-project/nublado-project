from django.utils.translation import gettext_lazy as _

BOT_MESSAGES = {
    'no_notes': _("bot.message.no_notes"),
    'notes_list': _("bot.message.notes_list {notes}"),
    'note_saved': _("bot.message.note_saved {note_tag}"),
    'note_removed': _("bot.message.note_removed {note_tag}"),
    'note_no_exist': _("bot.message.note_no_exist {note_tag}"),
    'note_no_content': _("bot.message.note_no_content"),
    'note_no_tag': _("bot.message.note_no_tag"),
    'note_no_args': _("bot.message.note_no_args"),
    'note_not_in_repo': _("bot.message.note_not_in_repo {note_tag}")
}