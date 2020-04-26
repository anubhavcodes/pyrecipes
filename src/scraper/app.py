from sys import argv

import yaml

from scraper.providers.hellofresh import HelloFreshScraper


def main(recipe_url: str):
    h = HelloFreshScraper(recipe_url)
    data = h.scrape()
    with open(data.get("name", "recipes.yml"), 'w') as f:
        yaml.dump(data, f)


if __name__ == '__main__':
    url = argv[-1]
    main(url)
