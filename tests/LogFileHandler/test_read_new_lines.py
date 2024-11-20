import pytest
from unittest.mock import patch, mock_open
from LogFileHandler import LogFileHandler


@pytest.fixture
def handler():
    return LogFileHandler(patterns=[], directory_path='./')


@patch('builtins.open', new_callable=mock_open, read_data='line1\nline2\n')
def test_read_new_lines_pass(mock_file, handler):
    handler.file_positions['test.log'] = 0

    result = handler.read_new_lines('test.log')

    assert result == ["line1\n", "line2\n"]
    mock_file.assert_called_once_with('test.log', 'r')


@patch('builtins.open', side_effect=IOError)
@patch('LogFileHandler.logger')
def test_read_new_lines_fail(mock_logger, mock_file, handler):
    handler.file_positions['test.log'] = 0

    result = handler.read_new_lines('test.log')

    assert result is None

    mock_logger.exception.assert_called_once_with(
        "Error occurred during reading a test.log"
    )
    mock_file.assert_called_once_with('test.log', 'r')
