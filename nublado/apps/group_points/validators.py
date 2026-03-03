from .constants import PointTransferError


def validate_point_transfer(sender, receiver):
    if sender.id == receiver.id:
        return PointTransferError.SELF

    if receiver.is_bot:
        return PointTransferError.BOT

    return None