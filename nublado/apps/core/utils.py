import re
import unicodedata
import markdown2


def remove_lead_and_trail_slash(s):
    if s.startswith("/"):
        s = s[1:]
    if s.endswith("/"):
        s = s[:-1]
    return s


def strip_outer_html_tags(s):
    """strips outer html tags"""

    start = s.find(">") + 1
    end = len(s) - s[::-1].find("<") - 1
    return s[start:end]


def markdown_to_html(text, strip_outer_tags=False, extras=["fenced-code-blocks"]):
    if not text:
        return ""
    html = markdown2.markdown(text, extras=extras)
    if strip_outer_tags:
        html = strip_outer_html_tags(html)
    return html


def slugify(
    value, separator: str = "-", allow_unicode: bool = False, lowercase: bool = True
) -> str:
    """
    This is a modified version of the slugify utility in Django.
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """

    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    if lowercase:
        value = value.lower()
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"[-\s]+", separator, value).strip("-_")
    return value
