import sys
import requests
from cssinj.console import Console
import re

class Scanner:
    def __init__(self):
        pass

    def get_input(self):
        pass

    def get_http_request(self):
        pass

    def get_url(self):
        pass

    def start(self, args):
        self.url = args.url
        self.headers = args.headers
        self.delay = args.delay
        self.cookie = args.cookie
        self.user_agent = args.user_agent

        
        headers = {}

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
        self.console.log("server", f"Starting scan of {self.url} with following config :")        
        for key, value in self.headers.items():
            self.console.log("connection_details", f"{key} : {value}")
