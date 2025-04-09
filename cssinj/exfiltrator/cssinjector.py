import asyncio
import signal
from cssinj.client import Clients
from cssinj.exfiltrator.server import Server


class CSSInjector:
    def __init__(self):
        self.clients = Clients()

    def start(self, args):
        self.server = Server(
            args=args,
            clients=self.clients
        )
        asyncio.run(self.server.start())

    def stop(self):
        self.server.stop()
