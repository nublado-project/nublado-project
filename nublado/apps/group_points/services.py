from django_telegram.models import TelegramChat, TelegramUser, TelegramGroupMember


async def transfer_points(tg_chat, tg_sender, tg_receiver, num_points):
    """
    Persist points transfer in the database.
    Returns sender_member, receiver_member group member objects from the ORM.
    """
    # TelegramChat ORM
    chat = await TelegramChat.objects.aget_or_create_from_telegram_chat(tg_chat)

    # TelegramUser ORM
    sender = await TelegramUser.objects.aget_or_create_from_telegram_user(tg_sender)
    receiver = await TelegramUser.objects.aget_or_create_from_telegram_user(tg_receiver)

    # TelegramGroupMember ORM
    sender_member, created = await TelegramGroupMember.objects.aget_or_create(
        user=sender,
        chat=chat,
    )
    receiver_member, created = await TelegramGroupMember.objects.aget_or_create(
        user=receiver,
        chat=chat,
    )

    # Increment points
    receiver_member.points += num_points
    await receiver_member.asave()

    return sender_member, receiver_member