from telegram.constants import ChatType, ChatMemberStatus


# Helper functions
def _is_group(tg_chat):
    return tg_chat.type in {ChatType.GROUP, ChatType.SUPERGROUP}


def _is_private(tg_chat):
    return tg_chat.type == ChatType.PRIVATE