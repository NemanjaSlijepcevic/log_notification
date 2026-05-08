import requests
import logging

logger = logging.getLogger(__name__)


MAX_MESSAGE_LENGTH = 4096


def send_telegram_message(bot_token: str, chat_id: str, message: str) -> bool:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    chunks = [
        message[i:i + MAX_MESSAGE_LENGTH]
        for i in range(0, len(message), MAX_MESSAGE_LENGTH)
    ]
    try:
        for chunk in chunks:
            response = requests.post(
                url, data={'chat_id': chat_id, 'text': chunk}
            )
            response.raise_for_status()
        return True
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}", exc_info=True)
        return False
    except Exception:
        logger.exception(
            f"An unexpected error occurred during POST request to {url}"
        )
        return False
