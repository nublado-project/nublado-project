from django.utils.translation import get_language_from_path


def strip_language_prefix_from_path(path):
    """
    Strip the language prefix from a request url path.
    """
    # Get language prefix from path if it exists.
    language = get_language_from_path(path)
    # If a language is found, the path is prefixed with /language, e.g., "/es"
    if language:
        # Account for the preceding slash.
        path = path.removeprefix(f"/{language}")
    return path
