import pytest
from config_utils import (
    check_pattern_input_value_string,
    check_pattern_input_value_empty
)


class TestPatternInputValues:

    def test_check_pattern_input_value_string_fail(self, mocker):
        mock_logger = mocker.patch('config_utils.logger')
        mocker.patch('os.getenv', return_value=623)

        with pytest.raises(SystemExit) as e:
            check_pattern_input_value_string()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Defined pattern is not a string!"
        )

    def test_check_pattern_input_value_string_pass(self, monkeypatch, mocker):
        monkeypatch.setenv("NOTIFICATION_PATTERNS", "random_chat_id")

        result = check_pattern_input_value_string()
        assert result, "check_pattern_input_value_string() exited unexpectedly"

    def test_check_pattern_input_value_empty_fail(self, monkeypatch, mocker):
        monkeypatch.setenv("NOTIFICATION_PATTERNS", "")
        mock_logger = mocker.patch('config_utils.logger')
        with pytest.raises(SystemExit) as e:
            check_pattern_input_value_empty()
        assert e.type == SystemExit
        assert e.value.code == 1

        mock_logger.error.assert_called_once_with(
            "Defined pattern is empty!"
        )

    def test_check_pattern_input_value_empty_pass(self, monkeypatch, mocker):
        monkeypatch.setenv("NOTIFICATION_PATTERNS", "random_chat_id")

        result = check_pattern_input_value_empty()
        assert result, "check_pattern_input_value_empty() exited unexpectedly"
