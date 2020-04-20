from typing import List, Set

import attr
from bs4 import BeautifulSoup
import requests


@attr.s
class BaseScraper:
    url = attr.ib(type=str)
    headers = {"User-Agent": "github.com/anubhavcodes/pyrecipes"}

    def get_soup(self):
        r = requests.get(self.url, headers=self.headers)
        return BeautifulSoup(r.text, 'html.parser')

    def scrape(self):
        raise NotImplementedError


class HelloFreshScraper(BaseScraper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soup = self.get_soup()

    def scrape(self):
        return {
            'name': self.name,
            'ingredients': self.ingredients,
            'nutrition': self.nutrition,
            'directions': self.directions
        }

    @property
    def name(self) -> str:
        title = self.soup.find('h1').text
        name = self.soup.find('h4').text
        return title + ' ' + name

    @property
    def ingredients(self) -> List[str]:
        parent_tag = self.soup.find('div', {'data-test-id': 'recipeDetailFragment.ingredients'})
        div = list(parent_tag)[3]
        in_the_box = [tag.text for tag in list(div.children)[0]]  # @TODO return sth like [{'name': .., 'quantity'}]
        div = list(parent_tag)[4]
        in_your_pantry = [tag.text for tag in list(div.children)[0]]
        return in_the_box + in_your_pantry

    @property
    def nutrition(self) -> List[str]:
        parent_tag = self.soup.find('div', {'data-test-id': 'recipeDetailFragment.nutrition-values'})
        div = list(parent_tag)[-1]
        return [tag.text for tag in list(div.children)[0]]

    @property
    def directions(self) -> List[str]:
        tag = self.soup.find('a', {'data-test-id': 'recipeDetailFragment.instructions.downloadLink'})
        div = list(tag.parents)[0]
        all_directions = set([t.text for t in div.next_sibling.next_sibling.find('div').findAll('div') if t.text])
        return sorted([x for x in all_directions if len(x) > 5 and x[0].isdigit()], key=lambda x: int(x[0]))
