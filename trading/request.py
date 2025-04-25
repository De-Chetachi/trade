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


key = "TWITTER_TOKEN"
token = os.environ.get(key)
if not token:
    print("set twitter api key")
    sys.exit()
bearer = f"Bearer {token}"
headers = {"Authorization": bearer, "Content-Type": "application/json"}


#url = f"https://api.twitter.com/2/users/:id" based on id
def get_user_id(username):
    """returns a users id given their username"""
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    r = requests.get(url, headers=headers)
    user_data = r.json();
    if r.status_code != 200:
        print(user_data)
        sys.exit()
    user_id = user_data["data"]["id"]
    return user_id


def interval(days):
    """return start and stop dates"""
    now = datetime.datetime.now(pytz.utc)
    compare_date = now - timedelta(days=days)
    [compare_date_, zone] = compare_date.isoformat().split(".")
    [now_, now_z] = now.isoformat().split(".")

    if "+" in zone:
        imp = zone.split("+")[1]
        compare_date_ += f"+{imp}"

        now_imp = now_z.split("+")[1]
        now_ += f"+{now_imp}"
        return (compare_date_, now_)
    
    elif "-" in zone:
        imp = zone.split("-")[1]
        compare_date_ += f"-{imp}"

        now_imp = now_z.split("-")[1]
        now_ += f"-{now_imp}"
        return (compare_date_, now_)
    return(compare_date_, now_)

def tweet_manu(username, coin, ticker, ca, id_, tweet):
    """manupulates the tweet"""
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
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
        except Exception as e:
            print(e)

def cas(tweet):
    """retrieves the cas """
    #pattern = "[^\s][1-9A-HJ-NP-Za-km-z]{32,44}[$\s\.,]|\$[A-Z]+[\s$\.,]"



def posts(username, coin, ticker, days):
    """retrieves tweet"""
    name = coin.replace("$", "").capitalize()
    id_, ca  = get_id_ca(name)
    user_id = get_user_id(username)
    posts_url = f"https://api.twitter.com/2/users/{user_id}/tweets" 
    compare_date, now = interval(days)
    params = {
        #"exclude": "replies,retweets"
        "start_time": compare_date,
        "end_time": now,
        "tweet.fields": "created_at"
        }
    res_posts = requests.get(posts_url, headers=headers, params=params)
    posts = res_posts.json()
    print(posts)
    if res_posts.status_code != 200:
        print(posts)
        sys.exit()
    while 1:
        tweets = posts["data"]
        for tweet in tweets:
            tweet_manu(username, coin, ticker, ca, id_, tweet)
        print_pretty()
        if posts["meta"].get("next_token"):
            params["pagination_token"] = posts["meta"]["next_token"]
            res_posts = requests.get(posts_url, headers=headers, params=params)
            posts = res_posts.json()
            if res_posts.status_code != 200:
                print(posts)
                sys.exit()
        else:
            break

