from abc import ABC, abstractmethod

from cssinj.client import Client


class BaseExfiltrationStrategy(ABC):
    """Base class for all exfiltration strategies."""

    name: str = 'base'

    def __init__(
        self,
        hostname: str,
        port: int,
        element: str = 'input',
        attribute: str = 'value',
        timeout: float = 3.0,
    ) -> None:
        self.hostname = hostname
        self.port = port
        self.element = element
        self.attribute = attribute
        self.timeout = timeout

    @abstractmethod
    def generate_start_payload(self, client: Client) -> str:
        """CSS returned on /start for this client."""

    @abstractmethod
    def generate_next_payload(self, client: Client) -> str:
        """CSS returned on /n for this client."""

    @abstractmethod
    def handle_valid(self, client: Client, data: str) -> str:
        """Called when /v receives data."""

    @abstractmethod
    def handle_end(self, client: Client) -> str:
        """Called when exfiltration is complete. Returns the response body."""
