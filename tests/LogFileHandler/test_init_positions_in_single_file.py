import pytest
from unittest.mock import patch, mock_open
from LogFileHandler import LogFileHandler


@pytest.fixture
def handler():
    return LogFileHandler(patterns=[], directory_path='.')


@patch('builtins.open', new_callable=mock_open, read_data='test')
def test_init_positions_in_single_file_pass(mock_open, handler, tmp_path):
    filename = tmp_path / "test.log"
    filename.write_text("test")

    mock_file = mock_open.return_value
    mock_file.tell.return_value = len("test")

    result = handler.init_positions_in_single_file(str(filename))

    assert result == 4
    mock_open.assert_called_once_with(str(filename), 'r')


@patch('builtins.open', side_effect=PermissionError)
@patch('LogFileHandler.logger')
def test_init_positions_in_single_file_permission_error(
        mock_logger, mock_open, handler):
    filename = 'test.log'

    result = handler.init_positions_in_single_file(filename)

    assert result is None

    mock_logger.warning.assert_called_once_with(
        f"Permission denied while reading file: {filename}"
    )
    mock_open.assert_called_once_with(filename, 'r')


@patch('builtins.open', side_effect=IOError)
@patch('LogFileHandler.logger')
def test_init_positions_in_single_file_exception(
        mock_logger, mock_open, handler):
    filename = 'test.log'

    result = handler.init_positions_in_single_file(filename)

    assert result is None

    mock_logger.exception.assert_called_once_with(
        f"Error occurred during initialization of {filename}"
    )
    mock_open.assert_called_once_with(filename, 'r')
