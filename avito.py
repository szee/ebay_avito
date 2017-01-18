'''
This one takes the keywords and searches avito for product names, prices and maybe urls of items.
'''

from bs4 import BeautifulSoup
from urllib.request import urlopen
import itertools

'''
The function gets a space separated keywords, replaces spaces with "+" and constructs the url to pass in to
the parsing part. Returns two bs4.element.ResultSet, one for the product name, another for it's price.
'''
def avito_search_by_keywords(keywords):
    formatted_keywords = keywords.replace(" ", "+")
    url = "https://www.avito.ru/moskva?q=" + formatted_keywords
    avito_code = urlopen(url).read()
    raw = BeautifulSoup(avito_code, 'lxml')
    item_name = raw.find_all("a", class_="item-description-title-link")
    item_price = raw.find_all("div", class_="about")

    item_name_str = [name_str.string for name_str in item_name]
    item_price_str = [price_str.string for price_str in item_price]

    return item_name_str, item_price_str

item_name, item_price = avito_search_by_keywords("canon 6d")
for item, price in itertools.zip_longest(item_name, item_price):
    print(item, "\n", price, end="\n=====================\n")

#Next step is to iterate through all the pages found for given keywords using link
#https://www.avito.ru/moskva?p=6&q=canon+6d
