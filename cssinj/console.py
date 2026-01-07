import datetime
from enum import Enum


class LogLevel(Enum):
    SERVER = "🛠️"
    EXFILTRATION = "🔎"
    END_EXFILTRATION = "✅"
    CONNECTION = "🌐"
    CONNECTION_DETAILS = "⚙️"
    ERROR = "❌"


class Console:
    @staticmethod
    def log(level: LogLevel, message: str):
        now = datetime.datetime.now()
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {level.value} {message}")

    @staticmethod
    def error_handler(exception: Exception, context: dict):
        Console.log(LogLevel.ERROR, str(exception))
