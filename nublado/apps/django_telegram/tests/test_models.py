import pytest

from telegram.constants import ChatType

from django_telegram.models import (
    TelegramUser,
    TelegramChat,
    TelegramGroupMember,
    TelegramGroupSettings,
)
from core.models import TimestampModel, LanguageModel


@pytest.fixture
def telegram_user():
    return TelegramUser.objects.create(
        telegram_id=123,
        username="fooman",
    )


@pytest.fixture
def telegram_chat():
    return TelegramChat.objects.create(
        telegram_id=456,
        chat_type=TelegramChat.TelegramChatType.GROUP,
        title="Foo Test Group",
    )


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
        assert user.date_created <= user.date_updated

    def test_str_representation(self):
        """
        __str__ returns username, or telegram_id if username doesn't exist.
        """

        # No username. The string value is telegram_id.
        user_no_username = TelegramUser.objects.create(telegram_id=123)
        assert str(user_no_username) == "123"

        # The string value is username.
        user_with_username = TelegramUser.objects.create(telegram_id=333, username="foo")
        assert str(user_with_username) == "foo"


class TestTelegramChat:
    """
    Tests for the TelegramChat model.
    """
    pytestmark = pytest.mark.django_db

    def test_pk(self):
        """
        telegram_id is the primary key
        """
        assert TelegramChat._meta.pk.name == "telegram_id"
    
    @pytest.mark.parametrize(
        "chat_type",
        TelegramChat.TelegramChatType.values,
    )
    def test_chat_type_choices(self, chat_type):
        """
        The TelegramChatType enum values can be saved and retrieved correctly.
        """
        chat = TelegramChat.objects.create(
            telegram_id=1,
            chat_type=chat_type,
        )
        chat.refresh_from_db()
        assert chat.chat_type == chat_type


    def test_create_chat_defaults(self):
        """
        Create a TelegramChat object and check its default values.
        """
        chat = TelegramChat.objects.create(
            telegram_id=456,
            chat_type=TelegramChat.TelegramChatType.GROUP,
            title="Foo Group",
        )
        assert chat.telegram_id == 456
        assert chat.title == "Foo Group"
        assert chat.chat_type == TelegramChat.TelegramChatType.GROUP
        assert chat.date_created is not None
        assert chat.date_updated is not None
        assert chat.date_created <= chat.date_updated

    def test_str_representation(self):
        """
        __str__ returns 'chat_type: telegram_id'.
        """
        chat = TelegramChat.objects.create(
            telegram_id=456,
            chat_type=TelegramChat.TelegramChatType.GROUP,
            title="Foo Group",
        )
        assert str(chat) == f"{chat.chat_type}:{chat.telegram_id}"


class TestTelegramGroupMember:
    """
    Tests for the TelegramGroupMember model.
    """

    def test_is_subclass(self):
        """
        The inheritance setup is OK.
        """
        classes = [
            TimestampModel,
        ]
        for class_name in classes:
            assert issubclass(TelegramGroupMember, class_name)



class TestTelegramGroupSettings:
    """
    Tests for the TelegramGroupSettings model.
    """
    
    def test_is_subclass(self):
            """
            The inheritance setup is OK.
            """
            classes = [
                TimestampModel,
                LanguageModel
            ]
            for class_name in classes:
                assert issubclass(TelegramGroupSettings, class_name)




