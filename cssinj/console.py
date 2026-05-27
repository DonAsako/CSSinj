"""Logging facade for cssinj.

Two paths share the same `cssinj` logger:

- `Console.log(LogLevel.X, msg)` — semantic events with emoji prefix (CLI UX).
- `logging.getLogger(__name__)` — used directly by library code.

Both go through the standard `logging` module, so handlers/formatters
configured by `setup_logging` apply uniformly.
"""

import logging
import sys
from enum import Enum
from pathlib import Path

LOGGER_NAME = 'cssinj'
EMOJI_FIELD = 'emoji'

_LOGGER = logging.getLogger(LOGGER_NAME)


class LogLevel(Enum):
    """Semantic categories surfaced in the terminal (emoji + log level)."""

    SERVER = ('🛠️', logging.INFO)
    EXFILTRATION = ('🔎', logging.DEBUG)
    END_EXFILTRATION = ('✅', logging.INFO)
    CONNECTION = ('🌐', logging.INFO)
    CONNECTION_DETAILS = ('⚙️', logging.DEBUG)
    ERROR = ('❌', logging.ERROR)

    def __init__(self, emoji: str, level: int) -> None:
        self.emoji = emoji
        self.level = level


# ANSI colors for TTY output. Disabled automatically when stderr is not a TTY.
_ANSI_RESET = '\033[0m'
_ANSI_BY_LEVEL: dict[int, str] = {
    logging.DEBUG: '\033[2;37m',  # dim grey
    logging.INFO: '\033[0;36m',  # cyan
    logging.WARNING: '\033[0;33m',  # yellow
    logging.ERROR: '\033[0;31m',  # red
    logging.CRITICAL: '\033[1;31m',  # bold red
}


class _ConsoleFormatter(logging.Formatter):
    """Pretty formatter for TTY output: `[ts] LEVEL emoji message`."""

    def __init__(self, use_color: bool) -> None:
        super().__init__(
            fmt='[%(asctime)s] %(levelname)-7s %(emoji)s %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S',
        )
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, EMOJI_FIELD):
            record.emoji = ' '
        text = super().format(record)
        if self.use_color:
            color = _ANSI_BY_LEVEL.get(record.levelno, '')
            if color:
                text = f'{color}{text}{_ANSI_RESET}'
        return text


class _FileFormatter(logging.Formatter):
    """Plain formatter for file output: stable, parseable, no color/emoji."""

    def __init__(self) -> None:
        super().__init__(
            fmt='%(asctime)s %(levelname)s %(name)s %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z',
        )


def setup_logging(
    *,
    quiet: bool = False,
    verbose: bool = False,
    log_file: Path | None = None,
) -> None:
    """Configure the cssinj root logger. Call once from the CLI entry point.

    Precedence: quiet > verbose > default INFO.
    """
    if quiet:
        level = logging.WARNING
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    # Reset existing handlers — supports being called twice in tests.
    for h in list(_LOGGER.handlers):
        _LOGGER.removeHandler(h)
        h.close()

    stream = logging.StreamHandler(sys.stderr)
    stream.setFormatter(_ConsoleFormatter(use_color=sys.stderr.isatty()))
    _LOGGER.addHandler(stream)

    if log_file is not None:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(_FileFormatter())
        _LOGGER.addHandler(file_handler)

    _LOGGER.setLevel(level)
    _LOGGER.propagate = False


class Console:
    """Thin façade for emitting categorised events from CLI-facing code."""

    @staticmethod
    def log(level: LogLevel, message: str) -> None:
        _LOGGER.log(level.level, message, extra={EMOJI_FIELD: level.emoji})

    @staticmethod
    def error_handler(exception: Exception, context: dict[str, str] | None = None) -> None:
        suffix = f" [{', '.join(f'{k}={v}' for k, v in context.items())}]" if context else ''
        Console.log(LogLevel.ERROR, f'{exception}{suffix}')
