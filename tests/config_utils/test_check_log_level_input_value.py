import os
import pytest
from unittest.mock import patch
from config_utils import check_log_level_input_value


class TestLogLevelInputVariables:

    def test_check_log_level_error(self, monkeypatch):
        monkeypatch.setenv("LOG_LEVEL", "not_working")
        with patch('config_utils.logger') as mock_logger:
            assert os.getenv("LOG_LEVEL") == "not_working"
            with pytest.raises(SystemExit) as e:
                check_log_level_input_value()
        assert e.type == SystemExit
        assert e.value.code == 1
        mock_logger.error.assert_called_once_with(
            "Invalid log level: 'NOT_WORKING'."
        )

    def test_check_log_level_success(self, monkeypatch):
        monkeypatch.setenv("LOG_LEVEL", "WARNING")
        result = check_log_level_input_value()
        assert result, "check_log_level_input_value() exited unexpectedly"
