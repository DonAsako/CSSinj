import sys
import requests
import re
from cssinj.console import Console
from cssinj.scanner.crawler import Crawler


class Scanner:
    def __init__(self):
        pass

    def analyze_response(self, response):
        headers = response.headers
        cookies = response.cookies
        # https://developer.mozilla.org/fr/docs/Web/HTTP/Reference/Headers check if one header is not in the list

    def start(self, args):
        self.url = args.url
        self.headers = args.headers
        self.delay = args.delay
        self.cookie = args.cookie
        self.user_agent = args.user_agent
        self.endpoint = []

        headers = {}

        if headers:
            # clean header
            for header in self.headers:
                key, value = header.split(":", maxsplit=1)
                key = re.sub(" +", "", key)
                value = re.sub(r"^\s+", "", value)
                headers[key] = value

        self.headers = headers

        if self.cookie:
            self.headers["cookie"] = "; ".join(self.cookie)

        # Overwrite Headers
        if self.user_agent:
            self.headers["user-agent"] = self.user_agent

        self.console = Console()

        # show config to user
        self.console.log(
            "server", f"Starting scan of {self.url} with following config :"
        )

        for key, value in self.headers.items():
            self.console.log("connection_details", f"{key} : {value}")

        # self.analyze_response(requests.get(self.url))
        crawler = Crawler(self.url)
        self.queue = crawler.search("input", "")
        for link in self.queue:
            print(f"Found {link} !")
        print(f"We have {len(self.queue)} links to analyse")
