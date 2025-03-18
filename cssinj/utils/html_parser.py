from html.parser import HTMLParser
import requests

class HtmlParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
        print(attrs)

parser = HtmlParser()
parser.feed(requests.get("http://127.0.0.1:5000/").content.decode("UTF-8"))