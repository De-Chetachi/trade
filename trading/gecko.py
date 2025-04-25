#!/usr/bin/env python3
import requests
import datetime
from datetime import timedelta
import os
import sys

gecko_key = "GECKO_KEY"
gecko_value = os.environ.get(gecko_key)
if not gecko_value:
    raise Exception("set the GECKO_KEY environment variable")
    
headers = {"accept": "application/json", "x_cg_api_key": gecko_value}
#headers = {"accept": "application/json", "x-cg-pro-api-key": gecko_value}
params = {"include_platform": "true"}
def get_id_ca(name):
    """returns the id of a coin given the name"""
    try:
        id_url = "https://api.coingecko.com/api/v3/coins/list"
        #id_url = "https://pro-api.coingecko.com/api/v3/coins/list"
        r = requests.get(id_url, headers=headers, params=params)
        if r.status_code != 200:
            print(r.json().get("status").get("error_message"))
            sys.exit()
        coins = r.json()
        for coin in coins:
            if coin["name"] == name: #this name shuld not contain the dollar sign:
                id_ = coin["id"]
                platforms = coin["platforms"]
                ca = "no ca"
                for key, value in platforms.items():
                    ca = value
                    break
                return (id_, ca)
    except Exception as e:
        print(e)


def get_prices(id_, start, end):
    """this endpoint retrieves the prices of a coin from start time to an end_time"""
    
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{id_}/market_chart/range"
        #url = f"https://pro-api.coingecko.com/api/v3/coins/{id_}/market_chart/range"
        parameters = {
            #"interval": "5m",
            "vs_currency": "usd",
            "from": start,
            "to": end,
            #"precision": "2"
        }
        r = requests.get(url, headers=headers, params=parameters)
        if r.status_code != 200:
            print(r.json().get("status").get("error_message"))
            sys.exit()
        prices = r.json().get("prices")
        prices_ = [price[1] for price in prices]
        return prices_
    except Exception as e:
        print(e)
