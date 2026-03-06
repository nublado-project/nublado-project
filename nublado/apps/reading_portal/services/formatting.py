def format_portal_intro(portal):
    header = "Welcome to the <b><i>Reading Portal</i></b>."
    description = portal.description or ""

    return f"{header}\n\n{description}"


def format_reading(reading):
    language = reading.language.upper()
    header = f"🌧 <b>Reading: {language}</b>"

    return f"{header}\n\n{reading.message_text}"


def format_portal_closed():
    return (
        "The <b><i>Reading Portal</i></b> has vanished.\n\n"
        "Please wait for the reading submissions to be reviewed "
        "and a new portal to appear. Thanks."
    )