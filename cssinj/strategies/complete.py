from cssinj.strategies.base import BaseExfiltrationStrategy


class CompleteStrategy(BaseExfiltrationStrategy):
    """
    Complete exfiltration strategy.
    Exfiltrates the complete DOM structure of the HTML.
    """

    name = "complete"

    def __init__(
        self,
        hostname: str,
        port: int,
        element: str = "*",
        attribut: str = "value",
        timeout: float = 3.0,
    ) -> None:
        super().__init__(hostname, port, timeout)
        self.element = element
        self.attribut = attribut

    def generate_start_payload(self, client) -> str:
        return "start"

    def generate_next_payload(self, client) -> str:
        return "next"

    def handle_valid(self, client, data: str) -> str:
        return "valid"

    def handle_end(self, client) -> None:
        return "end"
