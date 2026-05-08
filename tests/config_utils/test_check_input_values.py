import pytest
from unittest.mock import patch
from config_utils import check_input_values


class TestAllInputVariables:

    def test_check_inputs_success(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "random_api_token")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "random_chat_id")
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        assert check_input_values()

    def test_check_inputs_failed(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "random_api_token")
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "")
        monkeypatch.setenv("LOG_LEVEL", "WARNING")

        with patch('config_utils.logger') as mock_logger:
            with pytest.raises(SystemExit) as e:
                check_input_values()
        assert e.type == SystemExit
        assert e.value.code == 1
        mock_logger.error.assert_called_once_with("CHAT_ID is not set.")
