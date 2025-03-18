import sys
import requests
from cssinj.console import Console
import re
from bs4 import BeautifulSoup

class Scanner:
    def __init__(self):
        pass

    def analyze_response(self, response):
        headers = response.headers
        cookies = response.cookies
        soup = BeautifulSoup(response.content, 'html.parser')
        forms = soup.find_all("form") # Get All Form
        styles = soup.find_all("style") # Get All Style
        links = soup.find_all("link") # Get All Link
        for form in forms:
            action = form.get("action")
            if action:
                self.endpoint.append(action)

        for style in styles:
            self.endpoint.append(style)
        
        for link in links:
            print(link.get("rel"))
            if "stylesheet" in link.get("rel"):
                self.endpoint.append(link.get("href"))
        
        print(forms, styles, links)
        # https://developer.mozilla.org/fr/docs/Web/HTTP/Reference/Headers check if one header is not in the list
        
    def start(self, args):
        self.url = args.url
        self.headers = args.headers
        self.delay = args.delay
        self.cookie = args.cookie
        self.user_agent = args.user_agent
        self.endpoint = []
        
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

        self.analyze_response(requests.get(self.url))