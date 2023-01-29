import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('django')


class BotConfigManager(models.Manager):
    pass


class GroupMemberManager(models.Manager):
    def create_group_member(self, group_id=None, user_id=None, **kwargs):
        if not group_id:
            raise ValueError(_("Group id is required."))
        if not user_id:
            raise ValueError(_("User id is required."))

        group_member = self.model(
            group_id=group_id,
            user_id=user_id,
            **kwargs
        )
        group_member.full_clean()
        group_member.save(using=self._db)

        return group_member

    def create(self, group_id=None, user_id=None, **kwargs):
        return self.create_group_member(
            group_id=group_id,
            user_id=user_id
            **kwargs
        )

    def get_queryset(self):
        return super(GroupMemberManager, self).get_queryset()


    async def a_get_group_member(self, group_id: int, user_id: int):
        """Fetches a group member asynchronously."""
        try:
            group_member = await self.aget(
                group_id=group_id,
                user_id=user_id
            )
        except self.model.DoesNotExist:
            group_member = None

        return group_member


# class TmpMessageManager(models.Manager):
#     def create_tmp_message(self, message_id=None, chat_id=None, **kwargs):
#         if not message_id:
#             raise ValueError(_("Message id is required."))
#         if not chat_id:
#             raise ValueError(_("Chat id is required."))

#         tmp_message = self.model(
#             message_id=message_id,
#             chat_id=chat_id,
#             **kwargs
#         )
#         tmp_message.clean()
#         tmp_message.save(using=self._db)

#         return tmp_message

#     def create(self, message_id=None, chat_id=None, **kwargs):
#         return self.create_tmp_message(
#             message_id=message_id,
#             chat_id=chat_id,
#             **kwargs
#         )

#     def get_queryset(self):
#         return super(TmpMessageManager, self).get_queryset()