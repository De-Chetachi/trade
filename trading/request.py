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


#url = f"https://api.twitter.com/2/users/:id" based on id
url = f"https://api.twitter.com/2/users/by/username/{username}"
r = requests.get(url, headers=headers)
user_data = r.json();
user_id = user_data["data"]["id"]
print(user_id)
now = datetime.datetime.now(pytz.utc)
compare_date = now - timedelta(days=days_cap)


[compare_date_, zone] = compare_date.isoformat().split(".")
imp = zone.split("+")[1]
compare_date_ += f"+{imp}"

[now_, now_z] = now.isoformat().split(".")
now_imp = now_z.split("+")[1]
now_ += f"+{now_imp}"

posts_url = f"https://api.twitter.com/2/users/{user_id}/tweets" 
params = {
        #"exclude": "replies,retweets"
        "start_time": compare_date_,
        "end_time": now_,
        "tweet.fields": "created_at"
        }

res_posts = requests.get(posts_url, headers=headers, params=params)
posts = res_posts.json()
if res_posts.status_code != 200:
    print(posts)
    sys.exit()
#date_format = "%a %b %d %H:%M:%S %z %Y"
date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
name = coin.replace("$", "").capitalize()
id_, ca  = get_id_ca(name)
while 1:
    tweets = posts["data"]

    for tweet in tweets:
        print(tweet)
        date_str = tweet["created_at"]
        parsed_date = datetime.datetime.strptime(date_str, date_format)
        date = parsed_date.astimezone(pytz.utc)

        text = tweet["text"]
        pattern = re.compile(re.escape(ticker), re.IGNORECASE)
        match = pattern.search(text)

        if match:
            try:
                start = (date - timedelta(minutes=5)).timestamp()
                end = (date + timedelta(minutes=15)).timestamp()
                prices = get_prices(id_, start, end)

                add_doc(username, coin, date, prices[0], prices[1], prices[2], prices[3], ca)
                print_pretty()
            except Exception as e:
                print(e)
    if posts["meta"].get("next_token"):
        params["pagination_token"] = posts["meta"]["next_token"]
        res_posts = requests.get(posts_url, headers=headers, params=params)
        posts = res_posts.json()
        if res_posts.status_code != 200:
            print(posts)
            sys.exit()
    else:
        break

