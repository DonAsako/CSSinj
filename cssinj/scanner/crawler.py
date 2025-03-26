import re
from cssinj.utils.html_parser import HtmlParser


class Crawler:
    def __init__(self, start_url: str, requester):
        self.start_url = start_url
        self.requester = requester
        self.keep_urls = []
        self.visited_urls = []
        self.pending_urls = [start_url]
        self.base_url = self.get_base_url(start_url)
        self.keep_urls.append(self.base_url)
        if self.base_url not in self.pending_urls:
            self.pending_urls.append(self.base_url)

    def is_valid_url(self, url: str) -> str:
        return re.match(
            r"^https?:\/\/[a-zA-Z0-9-\.]+(?:\:[0-9]+)?(\/[^\s]*)?$",
            url,
        )

    def get_base_url(self, url: str) -> str:
        if self.is_valid_url(url):
            return re.search(r"^(https?:\/\/[a-zA-Z0-9.-]+(:\d+)?/)", url).group()

    def search(self, element_name: str = "", attribut_name: str = "") -> str:
        while len(self.pending_urls) != 0:
            for url in self.pending_urls:
                self.visite_url(url, (element_name, attribut_name))
                self.visited_urls.append(url)
                self.pending_urls.remove(url)

        return self.keep_urls

    def clean_url(self, url: str) -> str:
        url = re.sub(r"(?<=://)[/]+", "/", url)
        url = re.sub(r"(:\d+)(/)+", r"\1/", url)
        return url

    def keep_url(self, url, parser, filter):
        if filter[0] and not filter[1] and parser.get_element_by_name(filter[0]):
            self.keep_urls.append(url)
        elif filter[1] and not filter[0] and parser.get_element_by_name(filter[1]):
            self.keep_urls.append(url)
        elif (
            filter[0]
            and filter[1]
            and parser.get_element_by_name(filter[0])
            and parser.get_element_by_name(filter[1])
        ):
            self.keep_urls.append(url)
        elif not filter[0] and not filter[1]:
            self.keep_urls.append(url)

    def visite_url(self, url: str, filter: tuple) -> str:
        response = self.requester.get(url)
        html = response.text
        parser = HtmlParser()
        parser.feed(html)

        # save link filtered :
        links = parser.get_value_by_attr_name("href")

        # Append url to pending
        for link in links:
            if link.startswith(self.base_url):
                if link not in self.visited_urls + self.pending_urls:
                    url = self.clean_url(link)
                    self.pending_urls.append(url)
                    self.keep_url(url, parser, filter)
            if link.startswith("/") or link.startswith(".."):
                link = self.base_url + "/" + link
                url = self.clean_url(link)
                if url not in self.visited_urls + self.pending_urls:
                    self.pending_urls.append(url)
                    self.keep_url(url, parser, filter)
