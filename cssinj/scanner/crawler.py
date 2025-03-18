import re
import requests
from cssinj.utils.html_parser import HtmlParser


class Crawler:
    def __init__(self, start_url: str):
        self.start_url = start_url
        self.visited_urls = []
        self.pending_urls = [start_url]
        self.base_url = self.get_base_url(start_url)
        if self.base_url not in self.pending_urls:
            self.pending_urls.append(self.base_url)

    def is_valid_url(self, url: str) -> str:
        return re.match(
            r"^https?:\/\/[a-zA-Z0-9-\.]+(?:\:[0-9]+)?(\/[^\s]*)?$",
            url,
        )

    def get_base_url(self, url: str) -> str:
        if self.is_valid_url(url):
            return re.search(r"^(https?:\/\/[a-zA-Z0-9.-]+(:\d+)?)", url).group()

    def search(self):
        while len(self.pending_urls) != 0:
            for url in self.pending_urls:
                self.visite_url(url)
                self.pending_urls.remove(url)
                self.visited_urls.append(url)

    def visite_url(self, url: str) -> str:
        response = requests.get(url)


if __name__ == "__main__":
    crawler = Crawler("http://localhost:5000/admi?user=ok")
    crawler.search()
