import pytest
from unittest.mock import patch, Mock
import requests
from telegram_bot import send_telegram_message


@pytest.fixture
def mock_post():
    with patch('requests.post') as mock:
        yield mock


@pytest.fixture
def mock_logger():
    with patch('telegram_bot.logger') as mock:
        yield mock


def test_successful_message_send(mock_post):
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    bot_token = "valid_bot_token"
    chat_id = "valid_chat_id"
    message = "Hello, World!"

    response = send_telegram_message(bot_token, chat_id, message)

    mock_post.assert_called_once_with(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        data={'chat_id': chat_id, 'text': message}
    )
    assert response == mock_response.ok


def test_invalid_bot_token_handling(mock_post, mock_logger):
    bot_token = "invalid_token"
    chat_id = "123456"
    message = "Hello, World!"

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("404 Client Error")
    )
    mock_post.return_value = mock_response

    send_telegram_message(bot_token, chat_id, message)

    mock_logger.error.assert_called_once_with(
        "HTTP error occurred: 404 Client Error",
        exc_info=True
    )


def test_invalid_post_request(mock_post, mock_logger):
    bot_token = "valid_bot_token"
    chat_id = "valid_chat_id"
    message = "Hello, World!"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    mock_post.side_effect = Exception("Some unexpected error")

    send_telegram_message(bot_token, chat_id, message)

    mock_logger.exception.assert_called_once_with(
        f"An unexpected error occurred during POST request to {url}"
    )
