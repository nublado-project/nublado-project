import pytest

from django_telegram.models import TelegramUser


class TestTelegramUser:
    """
    Tests for the TelegramUser model.
    """

    pytestmark = pytest.mark.django_db

    def test_pk(self):
        """
        telegram_id is the primary key
        """
        assert TelegramUser._meta.pk.name == "telegram_id"

    def test_create_user_defaults(self):
        """
        Create a TelegramUser object and check its default values.
        """
        user = TelegramUser.objects.create(telegram_id=1)
        assert user.telegram_id == 1
        assert user.is_bot is False
        assert user.date_created is not None
        assert user.date_updated is not None

    def test_str_representation(self):
        """
        __str__ returns username, or telegram_id if username doesn't exist.
        """

        # No username. The string value is telegram_id.
        user_no_username = TelegramUser.objects.create(telegram_id=123)
        assert str(user_no_username) == "123"

        # The string value is username.
        user_with_username = TelegramUser.objects.create(
            telegram_id=333, username="foo"
        )
        assert str(user_with_username) == "foo"
