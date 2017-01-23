# coding: utf-8
'''
The bot returns average prices for items on ebay and avito found by keywords
'''

import urllib.request
import simplejson as json
import sys
import time
import telepot

from ebay import search_by_key_words
from avito import searching

def handle(msg):
    chat_id = msg["chat"]["id"]
    command = msg["text"]
    print("Got command: {}".format(command))

    #Handling the "/ebay" command. Returns average price for the product searched by keywords on ebay
    if command.startswith("/ebay "):
        keywords_ebay = command[6:]
        _, _, ebay_prices_rur = search_by_key_words(keywords_ebay, sys.argv[2])
        ebay_average_rur = sum(ebay_prices_rur) / len(ebay_prices_rur)

        bot.sendMessage(chat_id, "The average price on ebay is {}".format(ebay_average_rur))
    #Handling the "/avito" command. Returns average price for the product searched by keywords on avito
    elif command.startswith("/avito "):
        keywords_avito = command[7:]
        _, avito_prices = searching(keywords_avito)
        avito_average = sum(avito_prices) / len(avito_prices)

        bot.sendMessage(chat_id, "The average price on avito is {}".format(avito_average))
    #Handling "/help" command
    elif command == "/help":
        bot.sendMessage(chat_id, 'Type "/ebay keywords" to get the average price on ebay.\n' \
                                 'Type "/avito keywords" to get the average price on avito')

bot = telepot.Bot(sys.argv[1])
bot.message_loop(handle)
print ("Listening...")

while 1:
    time.sleep(10)
