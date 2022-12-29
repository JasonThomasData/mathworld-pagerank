import requests

class Browser:
    def __init__(self):
        self.browser = requests

    def get_content(self, page_url):
        return self.browser.get(page_url).content
