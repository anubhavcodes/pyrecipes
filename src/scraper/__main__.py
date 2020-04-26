from sys import argv

from scraper.app import main

url = argv[-1]
main(url)
