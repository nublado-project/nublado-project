from enum import Enum


# Generic default for PointsEngine if no bot-specific map is provided
# (e.g., 2 symbols for 1 point, three symbols for 2 points...).
DEFAULT_POINTS_MAP = {
    2: 1,
    3: 2,
    4: 4,
}


class PointTransferError(str, Enum):
    # When attempting to send points to oneself. 
    SELF = "self"
    # When attempting to send points to a bot.
    BOT = "bot"