from .constants import DEFAULT_POINTS_MAP, PointTransferError


class PointEngine:
    """
    A simple engine to parse point symbols, validate point transfers,
    and compute point values.
    """
    def __init__(self, *, point_symbol="+", points_map=None):
        # The point symbol prefix used in a reply to another group member's message
        # to award points (e.g., +).
        self.point_symbol = point_symbol

        # A dict that maps the number of point symbols to the respective number of points
        # (e.g, 2 symbols for 1 point, 3 symbols for 2 points).
        self.points_map = points_map or DEFAULT_POINTS_MAP

    def extract_points(self, text: str):
        """
        Get the number of point symbols at the beginning of a message and compute
        the corresponding point value.
        """
        if not text:
            return None

        text = text.strip()
        count = len(text) - len(text.lstrip(self.point_symbol))
        return self.points_map.get(count)

    def validate_point_transfer(self, tg_sender, tg_receiver):
        """
        Ensure sender and receiver are distinct group members, and not a bot.
        """
        if tg_sender.id == tg_receiver.id:
            return PointTransferError.SELF
        if tg_receiver.is_bot:
            return PointTransferError.BOT
        return None