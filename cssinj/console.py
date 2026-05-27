import logging
import sys
from enum import Enum

logger = logging.getLogger('cssinj')


class LogLevel(Enum):
    SERVER = ('🛠️', logging.INFO)
    EXFILTRATION = ('🔎', logging.INFO)
    END_EXFILTRATION = ('✅', logging.INFO)
    CONNECTION = ('🌐', logging.INFO)
    CONNECTION_DETAILS = ('⚙️', logging.DEBUG)
    ERROR = ('❌', logging.ERROR)

    def __init__(self, emoji: str, level: int) -> None:
        self.emoji = emoji
        self.level = level


def setup_logging(verbose: bool = False) -> None:
    """Configure the cssinj logger. Call once from the CLI entry point."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', '%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = False


class Console:
    @staticmethod
    def log(level: LogLevel, message: str) -> None:
        logger.log(level.level, '%s %s', level.emoji, message)

    @staticmethod
    def error_handler(exception: Exception, context: dict[str, str] | None = None) -> None:
        suffix = f" [{', '.join(f'{k}={v}' for k, v in context.items())}]" if context else ''
        Console.log(LogLevel.ERROR, f'{exception}{suffix}')
