import pytest
from unittest.mock import patch
from LogFileHandler import LogFileHandler


class Event:
    is_directory: bool
    src_path: str


@pytest.fixture
def handler():
    return LogFileHandler(patterns=[], directory_path='.')


def test_modified_directory(handler):
    event = Event()
    event.is_directory = True
    event.src_path = './directory.log'

    assert handler.on_modified(event) is None


def test_modified_incorrect_extension(handler):
    event = Event()
    event.is_directory = False
    event.src_path = './log.txt'

    assert handler.on_modified(event) is None


@patch(
    'LogFileHandler.LogFileHandler.init_positions_in_single_file',
    return_value=True
)
def test_modified_init(mock_init_positions, handler):
    event = Event()
    event.is_directory = False
    event.src_path = './test.log'

    assert handler.on_modified(event) is False
    mock_init_positions.assert_called_once_with('./test.log')


@patch(
    'LogFileHandler.LogFileHandler.read_new_lines',
    return_value=[]
)
@patch('LogFileHandler.send_telegram_message')
@patch('LogFileHandler.filter_patterns')
def test_no_new_lines(
    mock_filter_patterns,
    mock_send_telegram_message,
    mock_read_new_lines,
    handler
):
    handler.file_positions = {'./test.log': 0}

    event = Event()
    event.is_directory = False
    event.src_path = './test.log'

    assert handler.on_modified(event) is None

    mock_read_new_lines.assert_called_once_with('./test.log')
    mock_filter_patterns.assert_not_called()
    mock_send_telegram_message.assert_not_called()


@patch(
    'LogFileHandler.LogFileHandler.read_new_lines',
    return_value=['line1', 'line2']
)
@patch('LogFileHandler.send_telegram_message')
@patch(
    'LogFileHandler.filter_patterns',
    side_effect=lambda lines, patterns: lines
)
def test_modified_new_lines(
    mock_filter_patterns,
    mock_send_telegram_message,
    mock_read_new_lines,
    handler
):
    handler.file_positions = {'./test.log': 0}

    event = Event()
    event.is_directory = False
    event.src_path = './test.log'

    assert handler.on_modified(event) is None

    mock_read_new_lines.assert_called_once_with('./test.log')
    mock_filter_patterns.assert_called_once_with(['line1', 'line2'], [])
