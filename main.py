import logging
import time
import os
from watchdog.observers.polling import PollingObserver
from pattern_functions import generate_defined_patterns
from LogFileHandler import LogFileHandler
from config_utils import check_input_values


directory_path = './logs'
patterns = []
notify_patterns = os.getenv(
    'NOTIFICATION_PATTERNS', 'WARNING, EXCEPTION, ERROR, INFO'
)
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":

    check_input_values()
    patterns = generate_defined_patterns(notify_patterns)
    logger.debug(f"Found patterns: {patterns}")
    observer = PollingObserver()
    event_handler = LogFileHandler(patterns, directory_path)
    observer.schedule(event_handler, path=directory_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(300)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
