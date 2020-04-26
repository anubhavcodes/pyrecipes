from typing import Dict

from scraper.providers import BaseScraper


class HelloFreshScraper(BaseScraper):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soup = self.get_soup()

    def scrape(self) -> Dict:
        return {
            'name': self.name,
            'ingredients': self.ingredients,
            'nutritional_info': self.nutritional_info,
            'directions': self.directions,
            'source_url': self.url,
            'servings': '2 servings',
            'categories': ['HelloFresh'],
            'cook_time': self.cook_time,
        }

    @property
    def name(self) -> str:
        title = self.soup.find('h1').text
        name = self.soup.find('h4').text
        return title + ' ' + name

    @property
    def ingredients(self) -> str:
        parent_tag = self.soup.find('div', {'data-test-id': 'recipeDetailFragment.ingredients'})
        div = list(parent_tag)[3]
        in_the_box = [tag.text for tag in list(div.children)[0]]  # @TODO return sth like [{'name': .., 'quantity'}]
        div = list(parent_tag)[4]
        in_your_pantry = [tag.text for tag in list(div.children)[0]]
        return '\n'.join(in_the_box + in_your_pantry)

    @property
    def nutritional_info(self) -> str:
        parent_tag = self.soup.find('div', {'data-test-id': 'recipeDetailFragment.nutrition-values'})
        div = list(parent_tag)[-1]
        return '\n'.join([tag.text for tag in list(div.children)[0]])

    @property
    def directions(self) -> str:
        tag = self.soup.find('a', {'data-test-id': 'recipeDetailFragment.instructions.downloadLink'})
        div = list(tag.parents)[0]
        all_directions = set([t.text for t in div.next_sibling.next_sibling.find('div').findAll('div') if t.text])
        return '\n\n'.join(sorted([x for x in all_directions if len(x) > 5 and x[0].isdigit()], key=lambda x: int(x[0])))

    @property
    def cook_time(self) -> str:
        return self.soup.find('span', {'data-translation-id': 'recipe-detail.preparation-time'}).next.next.text
