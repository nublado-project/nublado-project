import logging

from telegram import Bot

from django.conf import settings
from django.utils.translation import activate, gettext as _

from ..models import GroupMember, BotConfig

logger = logging.getLogger('django')


def set_language(token):
    try:
        bot_config = BotConfig.objects.get(id=token)
        if bot_config.language in settings.LANGUAGES_DICT.keys():
            activate(bot_config.language)
        else:
            activate(settings.LANGUAGE_CODE)
    except BotConfig.DoesNotExist:
        activate(settings.LANGUAGE_CODE)


def update_group_members_from_admins(bot: Bot, group_id: int):
    """Updates group members in database with admins in telegram group."""
    try:
        group_admins = bot.get_chat_administrators(group_id)
        for group_admin in group_admins:
            user = group_admin.user
            group_member, group_member_created = GroupMember.objects.get_or_create(
                group_id=group_id,
                user_id=user.id
            )
        logger.info(GroupMember.objects.count())
        return GroupMember.objects.all()
    except:
        return None


def get_non_group_members(bot: Bot, group_id: int):
    """Returns "stragglers" that aren't currently part of a a group."""
    group_members = GroupMember.objects.filter(group_id=group_id).all()
    non_members = []
    if group_members:
        for group_member in group_members:
            try:
                member = bot.get_chat_member(group_id, group_member.user_id)
            except:
                non_members.append(group_member.user_id)
    logger.info(non_members)