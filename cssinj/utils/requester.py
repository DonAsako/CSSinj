import requests
import time
from cssinj.utils.error import ScannerError

class Requester:
    def __init__(self, headers: dict = {}, delay: int = 0):
        self.headers = headers
        self.delay = delay
        self.next_time = 0

    def get(self, url):
        self.wait()
        try:
            return requests.get(url, params={"headers": self.headers})
        except:
            raise ScannerError("Invalid URL")

    def wait(self):
        if self.next_time > int(time.time() * 1000):
            time.sleep((self.next_time - int(time.time() * 1000)) / 1000)

        self.next_time = int(time.time() * 1000) + self.delay
