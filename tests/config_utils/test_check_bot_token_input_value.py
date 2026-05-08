import pytest
from unittest.mock import patch
from config_utils import check_bot_token_input_value


class TestBotTokenInputValues:

    def test_check_bot_token_input_value_fail(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
        with patch('config_utils.logger') as mock_logger:
            with pytest.raises(SystemExit) as e:
                check_bot_token_input_value()
        assert e.type == SystemExit
        assert e.value.code == 1
        mock_logger.error.assert_called_once_with("BOT_TOKEN is not set.")

    def test_check_bot_token_input_value_pass(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "random_chat_id")
        result = check_bot_token_input_value()
        assert result, "check_bot_token_input_value() exited unexpectedly"
