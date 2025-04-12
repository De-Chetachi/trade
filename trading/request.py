#!/usr/bin/env python3

from collection import  add_doc
from pretty_data import print_pretty
import requests
import re
import sys
import datetime
import pytz
from datetime import timedelta
from gecko import get_id_ca, get_prices
import os

if len(sys.argv) < 5:
    print("provide all required arguments")
    sys.exit()
username = sys.argv[1]
coin = sys.argv[2]
ticker = sys.argv[3]
days_cap = int(sys.argv[4])
key = "TWITTER_TOKEN"
token = os.environ.get(key)
if not token:
    print("set twitter api key")
    sys.exit()
bearer = f"Bearer {token}"
headers = {"Authorization": bearer, "Content-Type": "application/json"}

params = {"tweet.fields": ["text", "created_at"]}

#url = f"https://api.twitter.com/2/users/:id" based on id
url = f"https://api.twitter.com/2/users/by/username/{username}"
r = requests.get(url, headers=headers, params=params)
data = r.json();
print(data)


tweets = data["includes"]["tweets"]

compare_date = datetime.datetime.now(pytz.utc) - timedelta(days=days_cap)

date_format = "%a %b %d %H:%M:%S %z %Y"

if not tweets or len(tweets) == 0:
    print("no tweets found")

for tweet in tweets:
    date_str = tweet["created_at"]
    parsed_date = datetime.datetime.strptime(date_str, date_format)
    date = parsed_date.astimezone(pytz.utc)

    if date >= compare_date:
        text = tweet["text"]
        pattern = re.compile(re.escape(ticker), re.IGNORECASE)
        match = pattern.search(text)

        if match:
            try:
                name = coin.replace("$", "").capitalize()
                id_, ca  = get_id_ca(name)

                start = date - timedelta(minutes=5)
                start = start.timestamp()
                end = date + timedelta(minutes=15)
                end = end.timestamp()
                prices = get_prices(id_, start, end)

                add_doc(username, coin, date_str, prices[0], prices[1], prices[2], prices[3], ca)
                print_pretty()
            except Exception as e:
                print(e)
