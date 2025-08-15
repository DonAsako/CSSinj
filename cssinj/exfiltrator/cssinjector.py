import asyncio
import signal
from cssinj.client import Clients
from cssinj.exfiltrator.server import Server
from cssinj.file import OutputFile


class CSSInjector:
    def __init__(self):
        self.clients = Clients()
        self.output_file = None

    def start(self, args):
        if args.output:
            self.output_file = OutputFile(args.output, self.clients)

        self.server = Server(
            args=args, clients=self.clients, output_file=self.output_file
        )
        asyncio.run(self.server.start())

    def stop(self):
        self.server.stop()
