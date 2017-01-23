'''
This one takes the keywords and searches avito for product names, prices and maybe urls of items.
'''

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import quote_plus
import itertools
from re import sub


'''
The function gets the opened URL. Returns two lists, one with product names, another with the prices.
'''
def parsing(avito_code):
    raw = BeautifulSoup(avito_code, 'lxml')
    item_names_raw = raw.find_all("a", class_="item-description-title-link")
    item_prices_raw = raw.find_all("div", class_="about")

    item_names = []
    item_prices = []

    for item, price in itertools.zip_longest(item_names_raw, item_prices_raw):
        try:
            item_prices.append(int(sub("[\s+]", "", price.string[:-11])))
            item_names.append(item.string.strip())
        except (TypeError, ValueError, AttributeError):
            continue

    return item_names, item_prices

'''
This one gets the keywords, iterates through all the available pages on avito for the request, calls the
"searching" for every page and adds up the results.
'''
def searching(keywords):
    formatted_keywords = keywords.replace(" ", "+")
    i = 1
    urls = []
    item_names = []
    item_prices = []
    while True:
        try:
            url = ("https://www.avito.ru/moskva?p={}&q={}".format(i, quote_plus(formatted_keywords)))
            iter_names, iter_prices = parsing(urlopen(url).read())
            item_names.extend(iter_names)
            item_prices.extend(iter_prices)
            i += 1
        except HTTPError:
            break

    return item_names, item_prices
