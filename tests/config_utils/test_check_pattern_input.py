import pytest
from unittest.mock import patch
from config_utils import (
    check_pattern_input_value_string,
    check_pattern_input_value_empty
)


class TestPatternInputValues:

    def test_check_pattern_input_value_string_fail(self):
        with patch('config_utils.logger') as mock_logger, \
             patch('os.getenv', return_value=623):
            with pytest.raises(SystemExit) as e:
                check_pattern_input_value_string()
        assert e.type == SystemExit
        assert e.value.code == 1
        mock_logger.error.assert_called_once_with(
            "Defined pattern is not a string!"
        )

    def test_check_pattern_input_value_string_pass(self, monkeypatch):
        monkeypatch.setenv("NOTIFICATION_PATTERNS", "random_chat_id")
        result = check_pattern_input_value_string()
        assert result, "check_pattern_input_value_string() exited unexpectedly"

    def test_check_pattern_input_value_empty_fail(self, monkeypatch):
        monkeypatch.setenv("NOTIFICATION_PATTERNS", "")
        with patch('config_utils.logger') as mock_logger:
            with pytest.raises(SystemExit) as e:
                check_pattern_input_value_empty()
        assert e.type == SystemExit
        assert e.value.code == 1
        mock_logger.error.assert_called_once_with("Defined pattern is empty!")

    def test_check_pattern_input_value_empty_pass(self, monkeypatch):
        monkeypatch.setenv("NOTIFICATION_PATTERNS", "random_chat_id")
        result = check_pattern_input_value_empty()
        assert result, "check_pattern_input_value_empty() exited unexpectedly"
