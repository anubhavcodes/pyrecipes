import attr
import requests
from bs4 import BeautifulSoup


@attr.s
class BaseScraper:
    url = attr.ib(type=str)
    headers = {"User-Agent": "github.com/anubhavcodes/pyrecipes"}

    def get_soup(self):
        r = requests.get(self.url, headers=self.headers)
        return BeautifulSoup(r.text, 'html.parser')

    def scrape(self):
        raise NotImplementedError
