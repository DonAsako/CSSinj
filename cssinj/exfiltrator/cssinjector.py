import argparse
import asyncio
import contextlib

from cssinj.client import Clients
from cssinj.exfiltrator.server import Server
from cssinj.file import OutputFile


class CSSInjector:
    def __init__(self) -> None:
        self.clients = Clients()
        self.output_file: OutputFile | None = None
        self.server: Server | None = None

    def start(self, args: argparse.Namespace) -> None:
        if args.output:
            self.output_file = OutputFile(args.output, self.clients)
        self.server = Server(args=args, clients=self.clients, output_file=self.output_file)
        with contextlib.suppress(KeyboardInterrupt):
            asyncio.run(self.server.run())
