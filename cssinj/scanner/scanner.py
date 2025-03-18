import sys
import re
from cssinj.console import Console
from cssinj.scanner.crawler import Crawler
from cssinj.utils.requester import Requester


class Scanner:
    def __init__(self):
        self.requester = Requester()

    def analyze_response(self, response):
        headers = response.headers
        cookies = response.cookies
        # Try to inject input
        # Try to inject headers
        # Try to check if different token

        # https://developer.mozilla.org/fr/docs/Web/HTTP/Reference/Headers check if one header is not in the list

    def start(self, args):
        self.url = args.url
        self.console = Console()

        try:
            delay = int(args.delay)
        except ValueError:
            print("Invalid delay !")
            exit(1)

        cookie = args.cookie
        user_agent = args.user_agent

        headers = {}

        if headers:
            # clean header
            for header in args.headers:
                key, value = header.split(":", maxsplit=1)
                key = re.sub(" +", "", key)
                value = re.sub(r"^\s+", "", value)
                headers[key] = value

        if args.cookie:
            headers["cookie"] = "; ".join(args.cookie)

        # Overwrite Headers
        if args.user_agent:
            headers["user-agent"] = args.user_agent

        # pass params to requester
        self.requester.headers = headers
        self.requester.delay = delay

        # show config to user
        self.console.log(
            "server", f"Starting scan of {self.url} with following config :"
        )

        for key, value in headers.items():
            self.console.log("connection_details", f"{key} : {value}")

        crawler = Crawler(self.url, self.requester)

        self.queue = crawler.search("input", "")
        print(f"We have {len(self.queue)} links in queue")
        for link in self.queue:
            resp = self.requester.get(link)
            print(resp.content)
            self.analyze_response(resp)
