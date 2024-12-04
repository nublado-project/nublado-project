import difflib
import re
import logging

from telegram import Message

from ..models import GroupMember

logger = logging.getLogger('django')

PUNCTUATION = ".,;:_-¿?¡!"


def tokenize(str, punctuation=False):
    if punctuation is True:
        for i in str:
            if i in PUNCTUATION:
                str = str.replace(i, " {} ".format(i))

    return re.split('\s+', str)


def untokenize(str):
    return " ".join(str)


def compare_strings(string_a, string_b):
    matcher = difflib.SequenceMatcher(
        a=tokenize(string_a, punctuation=True),
        b=tokenize(string_b, punctuation=True)
    )
    result_string_a = ""
    result_string_b = ""

    for tag, a_start, a_end, b_start, b_end in matcher.get_opcodes():
        if tag == "replace":
            substr = untokenize(matcher.a[a_start:a_end])
            result_string_a += "{}{}{}".format(
                " <s>" if substr not in PUNCTUATION else "<s>",
                substr,
                "</s>"
            )
            substr = untokenize(matcher.b[b_start:b_end])
            result_string_b += "{}{}{}".format(
                " <b>" if substr not in PUNCTUATION else "<b>",
                substr,
                "</b>"
            )
        elif tag == "equal":
            substr = untokenize(matcher.a[a_start:a_end])
            result_string_a += "{}".format(
                " " + substr if substr.strip() not in PUNCTUATION else substr
            )
            substr = untokenize(matcher.b[b_start:b_end])
            result_string_b += "{}".format(
                " " + substr if substr.strip() not in PUNCTUATION else substr
            )
        elif tag == "delete":
            substr = untokenize(matcher.a[a_start:a_end])
            result_string_a += "{}{}{}".format(
                " <s>" if substr.strip() not in PUNCTUATION else "<s>",
                substr,
                "</s>"
            )
        elif tag == "insert":
            substr = untokenize(matcher.b[b_start:b_end])
            result_string_b += "{}{}{}".format(
                " <b>" if substr.strip() not in PUNCTUATION else "<b>",
                substr,
                "</b>"
            )

    return result_string_a, result_string_b


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
