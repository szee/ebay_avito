'''
This one will make a call to ebay's API making search by keywords.
'''

import sys
import xml.etree.ElementTree as ET

'''
Function gets a space separated string of keywords e.g. "Canon 6D", replaces
the spaces with "%20" to match the API call format and lowercases it.
Returns response-type response on the API call.
'''


def search_by_key_words(keywords, app_name):
    import requests


    number_of_items = 5
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
    for child in ET.fromstring(search_results.text)[3]:
        try:
            item_prices.append(float(child[13][1].text))
            item_names.append(child[1].text)
        except ValueError:
            continue
        #print(child[1].text, float(child[13][1].text), end="\n")

    return item_names, item_prices

#The part to make an XML file just to take a look at the structure
#f = open("request.xml", "w")
#f.write(search_by_key_words("canon 6d").text)
#f.close()

'''
Finally decided to parse XML with ElementTree. Messing around with XML (getting product name, price, etc).
'''
items, prices = search_by_key_words("canon 6d", sys.argv[1])
print(items, prices)
