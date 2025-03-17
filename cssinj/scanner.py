import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scanner:
    def __init__(self):
        self.driver = None

    def get_input(self):
        self.driver = None

    def get_http_request(self):
        pass

    def get_url(self):
        pass

    def start(self, url):
        try:
            # Detach Browser For Debug
            options = Options()
            options.add_experimental_option("detach", True)

            # Use Chromium
            self.driver = webdriver.Chrome(options=options)

        except Exception as e:
            print(f"Error during driver initialization : {e}")
            sys.exit(1)

        self.driver.get(url)


    def quit(self):
        self.driver.quit()

