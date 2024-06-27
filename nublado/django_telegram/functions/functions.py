import difflib
import re
import logging

from telegram import Message

from ..models import GroupMember

logger = logging.getLogger('django')


def tokenize_string(string):
    return re.split('\s+', string)


def untokenize_string(string):
    return " ".join(string)


def compare_strings(string_a, string_b):
    string_a = tokenize_string(string_a)
    string_b = tokenize_string(string_b)

    matcher = difflib.SequenceMatcher(a=string_a, b=string_b)

    for tag, a_start, a_end, b_start, b_end in matcher.get_opcodes():
        if tag == "replace":
            for x in range(a_start, a_end):
                string_a[x] = "<s>{}</s>".format(string_a[x])
            for x in range(b_start, b_end):
                string_b[x] = "<b>{}</b>".format(string_b[x])
        elif tag == "delete":
            for x in range(a_start, a_end):
                string_a[x] = "<s>{}</s>".format(string_a[x])
        elif tag == "insert":
            for x in range(b_start, b_end):
                string_b[x] = "<b>{}</b>".format(string_b[x])

    string_a = untokenize_string(string_a)
    string_b = untokenize_string(string_b)

    print("{}\n{}".format(string_a, string_b))

    return string_a, string_b


def parse_command_last_arg_text(
    message: Message,
    maxsplit: int = 1
):
    """Returns the text for a command that receives text as its last arg"""
    # Message text is the command and given arguments (e.g., /command arg some text)
    message_text = message.text
    if maxsplit >= 1:
        command_and_args = message_text.split(None, maxsplit)
        if len(command_and_args) >= maxsplit + 1:
            arg_text = command_and_args[maxsplit]
            return arg_text
        else:
            return None
    else:
        return False
