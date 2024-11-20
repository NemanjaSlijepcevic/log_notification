import os
import logging


logger = logging.getLogger(__name__)


def check_bot_token_input_value():
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set.")
        exit(1)
    return True


def check_chat_id_input_value():
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    if not CHAT_ID:
        logger.error("CHAT_ID is not set.")
        exit(1)
    return True


def check_log_level_input_value():
    VALID_LOG_LEVELS = {
        "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    }
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    if log_level not in VALID_LOG_LEVELS:
        logger.error(f"Invalid log level: '{log_level}'.")
        exit(1)
    return True


def check_pattern_input_value_string():
    notify_patterns = os.getenv(
        'NOTIFICATION_PATTERNS', 'WARNING, EXCEPTION, ERROR, INFO'
    )
    if not isinstance(notify_patterns, str):
        logger.error("Defined pattern is not a string!")
        exit(1)
    return True


def check_pattern_input_value_empty():
    notify_patterns = os.getenv(
        'NOTIFICATION_PATTERNS', 'WARNING, EXCEPTION, ERROR, INFO'
    )
    if not notify_patterns:
        logger.error("Defined pattern is empty!")
        exit(1)
    return True


def check_input_values():
    check_bot_token_input_value()
    check_chat_id_input_value()
    check_pattern_input_value_string()
    check_pattern_input_value_empty()
    check_log_level_input_value()
    return True
