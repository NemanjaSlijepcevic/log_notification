import os
import logging
from watchdog.events import FileSystemEventHandler
from pattern_functions import filter_patterns
from telegram_bot import send_telegram_message

logger = logging.getLogger(__name__)
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


class LogFileHandler(FileSystemEventHandler):

    def __init__(self, patterns, directory_path):
        logger.debug("Init class:")
        self.patterns = patterns
        self.file_positions = {}
        if not os.path.isdir(directory_path):
            logger.warning(f"Log directory does not exist: {directory_path}")
            return
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) and file_path.endswith('.log'):
                self.init_positions_in_single_file(file_path)

    def init_positions_in_single_file(self, file_path):
        logger.debug(f"Init position in a file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(0, os.SEEK_END)
                self.file_positions[file_path] = f.tell()
                logger.info(
                    f"{file_path} start pos: {self.file_positions[file_path]}"
                )
                return self.file_positions[file_path]
        except PermissionError:
            logger.warning(
                f"Permission denied while reading file: {file_path}"
            )
            return None
        except Exception:
            logger.exception(
                f"Error occurred during initialization of {file_path}"
            )
            return None

    def read_new_lines(self, file_path):
        logger.debug(f"Reading new lines in a file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                last_position = f.seek(0, os.SEEK_END)
                f.seek(self.file_positions.get(file_path, 0))
                new_lines = f.readlines()
                self.file_positions[file_path] = last_position
                return new_lines
        except Exception:
            logger.exception(f"Error occurred during reading a {file_path}")
            return None

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.log'):
            return
        log_file = event.src_path
        logger.debug(f"File modified: {log_file}")
        if log_file not in self.file_positions:
            self.init_positions_in_single_file(log_file)
            return
        new_lines = self.read_new_lines(log_file)
        if not new_lines:
            logger.debug(f"No new lines in: {log_file}")
            return
        logger.debug(f"Found lines: {new_lines}")
        new_lines = filter_patterns(new_lines, self.patterns)
        logger.debug(f"Found patterns: {new_lines}")
        if new_lines:
            send_telegram_message(BOT_TOKEN, CHAT_ID, new_lines)
