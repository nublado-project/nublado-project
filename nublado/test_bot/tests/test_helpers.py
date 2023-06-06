import logging

import pytest

logger = logging.getLogger('django')


class TestGroupAdminCommands:
    @pytest.mark.asyncio
    async def test_is_group_member(self, tg_client):
        pass
