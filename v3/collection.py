#!/usr/bin/env python3

from database import get_db

dbname = get_db()
col_name = dbname["influencer_price_action"]

def add_doc(influencer, tweet_time, price_0m, price_5m, price_10m, price_15m, ca, coin):
    """adds a row to the influencer_price_action collection"""
    doc = {
            "influencer": influencer,
            "coin": coin,
            "ca": ca,
            "Tweet Time": tweet_time,
            "Price @0m": price_0m,
            "price @5m": price_5m,
            "price @10m": price_10m,
            "price @15m": price_15m,
            "% change": (float(price_15m) - float(price_0m)) / 100,
    }
    col_name.insert_one(doc)

def items():
    "return all the documents in a collection"
    return col_name.find({}, {  "_id": 0 })
