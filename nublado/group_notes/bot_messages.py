from django.utils.translation import gettext as _

BOT_MESSAGES = {
    'no_notes': _("There are no saved notes."),
    'notes_list': _("*Notes*\n{notes}"),
    'note_saved': _("The note *{note_tag}* has been saved."),
    'note_removed': _("The note *{note_tag}* has been removed."),
    'note_no_exist': _("The note *{note_tag}* doesn't exist."),
    'note_no_content': _("A note needs content."),
    'note_no_tag': _("A note must have a tag."),
    'note_no_args': _("A note needs a tag and content."),
    'note_not_in_repo': _(
        "The content for the note *{note_tag}* was not found in the repo."
    )
}