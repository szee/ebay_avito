'''
This one will make a call to ebay's API making search by keywords.
'''

import requests
import sys
import xml.etree.ElementTree as ET

'''
Function gets a space separated string of keywords e.g. "Canon 6D", replaces
the spaces with "%20" to match the API call format and lowercases it.
Returns response-type response on the API call.
'''


def search_by_key_words(keywords, app_name):
    number_of_items = 100
    formatted_keywords = keywords.replace(" ", "%20").lower()
    search_results = requests.get("http://svcs.ebay.com/services/search/FindingService/v1?" \
                                  "OPERATION-NAME=findItemsByKeywords&" \
                                  "SERVICE-VERSION=1.12.0&" \
                                  "SECURITY-APPNAME={}&" \
                                  "RESPONSE-DATA-FORMAT=XML&" \
                                  "REST-PAYLOAD&" \
                                  "keywords={}&" \
                                  "paginationInput.entriesPerPage={}".
                                  format(app_name, formatted_keywords, number_of_items))

    item_names = []
    item_prices = []
    item_prices_rur = []
    currency_dict = getting_currency_dict()

    for child in ET.fromstring(search_results.text)[3]:
        try:
            price_currency = float(child[13][1].text)
            currency_ticker = child[13][1].attrib["currencyId"]
            price_rur = price_currency * currency_dict[currency_ticker]
            item_name = child[1].text
            item_prices.append(price_currency)
            item_prices_rur.append(price_rur)
            item_names.append(item_name)
        except (ValueError, IndexError):
            continue

    return item_names, item_prices, item_prices_rur

def getting_currency_dict():
    currency_req = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
    currencies = ET.fromstring(currency_req.text)
    currency_dict = {rate[1].text:float(rate[4].text.replace( ",", ".")) for rate in currencies}
    return currency_dict
#The part to make an XML file just to take a look at the structure
#f = open("request.xml", "w")
#f.write(search_by_key_words("canon 6d").text)
#f.close()

'''
Finally decided to parse XML with ElementTree. Messing around with XML (getting product name, price, etc).
'''
