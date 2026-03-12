class ReadingPortalError(Exception):
    """Base exception for Reading Portal domain."""
    pass


class NoReplyToAudio(ReadingPortalError):
    pass


class NoReplyToReading(ReadingPortalError):
    pass


class NoAudioReplyToText(ReadingPortalError):
    pass


class NoOpenPortal(ReadingPortalError):
    pass


class NoDraftPortal(ReadingPortalError):
    pass


class OpenPortalExists(ReadingPortalError):
    pass


class EmptyPortal(ReadingPortalError):
    pass


class InvalidReadingLanguage(ReadingPortalError):
    pass


class AlreadySubmitted(ReadingPortalError):
    pass


class NoPendingReading(ReadingPortalError):
    pass
