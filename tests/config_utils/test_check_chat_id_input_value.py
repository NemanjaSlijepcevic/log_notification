import pytest
from unittest.mock import patch
from config_utils import check_chat_id_input_value


class TestChatIdInputValues:

    def test_check_chat_id_input_value_fail(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "")
        with patch('config_utils.logger') as mock_logger:
            with pytest.raises(SystemExit) as e:
                check_chat_id_input_value()
        assert e.type == SystemExit
        assert e.value.code == 1
        mock_logger.error.assert_called_once_with("CHAT_ID is not set.")

    def test_check_chat_id_input_value_pass(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "random_chat_id")
        result = check_chat_id_input_value()
        assert result, "check_chat_id_input_value() exited unexpectedly"
