from typing import Dict, List
from base64 import b64encode

import requests

from scraper.providers import BaseScraper
from scraper.providers.utils import format_measurements


class HelloFreshScraper(BaseScraper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.soup = self.get_soup()

    def scrape(self) -> Dict:
        return {
            "name": self.name + "-" + self.description,
            "ingredients": self.ingredients,
            "nutritional_info": self.nutritional_info,
            "directions": self.directions,
            "source_url": self.url,
            "servings": "2 servings",
            "categories": ["HelloFresh"],
            "prep_time": "10 minutes",
            "cook_time": self.cook_time,
            "total_time": self.cook_time,
            "photo": self.photo,
        }

    @property
    def name(self) -> str:
        return self.soup.find("h1").text

    @property
    def description(self) -> str:
        return self.soup.find("h4").text

    @property
    def ingredients(self) -> str:
        measurements = ["ml", "g", "Stück"]
        parent_tag = self.soup.find("div", {"data-test-id": "recipeDetailFragment.ingredients"})
        div = list(parent_tag)[3]
        in_the_box = [format_measurements(tag.text, measurements) for tag in list(div.children)[0]]
        div = list(parent_tag)[4]
        in_your_pantry = [tag.text for tag in list(div.children)[1]]
        return "\n".join(in_the_box + in_your_pantry)

    @property
    def nutritional_info(self) -> str:
        measurements = ["Portion", "(kJ)", "kcal)"]
        parent_tag = self.soup.find("div", {"data-test-id": "recipeDetailFragment.nutrition-values"})
        div = list(parent_tag)[-1]
        return "\n".join([format_measurements(tag.text, measurements) for tag in list(div.children)[0] if tag.text])

    @property
    def directions(self) -> str:
        tag = self.soup.find("a", {"data-test-id": "recipeDetailFragment.instructions.downloadLink"})
        div = list(tag.parents)[0]
        all_directions = set([t.text for t in div.next_sibling.next_sibling.find("div").findAll("div") if t.text])
        final_directions = sorted([x for x in all_directions if len(x) > 5 and x[0].isdigit()], key=lambda x: int(x[0]))
        return "\n\n".join([x[:1] + ". " + x[1:] for x in final_directions])

    @property
    def cook_time(self) -> str:
        return self.soup.find("span", {"data-translation-id": "recipe-detail.preparation-time"}).next.next.text

    @property
    def photo(self) -> str:
        url = self.soup.find("img", {"alt": self.name}).attrs["src"]
        r = requests.get(url, headers=self.headers)
        return HelloFreshScraper.get_b64_encoded_str(r.content)

    @property
    def step_image_urls(self) -> List[str]:
        all_images = [t.attrs.get("data-iesrc") for t in self.soup.findAll("picture")]
        step_images = [img for img in all_images if "step-" in img]
        return list(set(step_images))

    @staticmethod
    def get_b64_encoded_str(content: bytes) -> str:
        return b64encode(content).decode("utf-8")
