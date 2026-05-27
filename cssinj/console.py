import datetime
from enum import Enum


class LogLevel(Enum):
    SERVER = '🛠️'
    EXFILTRATION = '🔎'
    END_EXFILTRATION = '✅'
    CONNECTION = '🌐'
    CONNECTION_DETAILS = '⚙️'
    ERROR = '❌'


class Console:
    @staticmethod
    def log(level: LogLevel, message: str) -> None:
        now = datetime.datetime.now()
        print(f'[{now:%Y-%m-%d %H:%M:%S}] {level.value} {message}')

    @staticmethod
    def error_handler(exception: Exception, context: dict[str, str] | None = None) -> None:
        suffix = f" [{', '.join(f'{k}={v}' for k, v in context.items())}]" if context else ''
        Console.log(LogLevel.ERROR, f'{exception}{suffix}')
