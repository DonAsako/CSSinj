from abc import ABC, abstractmethod


class BaseExfiltrationStrategy(ABC):
    """Base class for all exfiltration strategies."""

    name: str = "base"

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        self.port = port

    @abstractmethod
    def generate_start_payload(self, client) -> str:
        """CSS returned on /start for this client."""
        ...

    @abstractmethod
    def generate_next_payload(self, client) -> str:
        """CSS returned on /n for this client."""
        ...

    @abstractmethod
    def handle_valid(self, client, data: str) -> str:
        """Called when /v receives data."""
        ...

    @abstractmethod
    def handle_end(self, client) -> None:
        """Called when exfiltration is complete for this client."""
        ...
