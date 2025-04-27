#!/usr/bin/env python3

from collection import  add_doc
from pretty_data import print_pretty
import requests
import re
import sys
import datetime
import pytz
from datetime import timedelta
from gecko import get_ca, get_name, get_prices
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
    user_data = r.json()
    if r.status_code != 200:
        print(user_data)
        return None
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


#pattern_ = "(?<=^|\s)[1-9A-HJ-NP-Za-km-z]{32,44}(?=$|[\s.,])|(?<=^|\s)\$[A-Z]+(?=$|[\s.,])"
pattern_ ="(?<=^)[1-9A-HJ-NP-Za-km-z]{32,44}(?=$|[\s.,])|(?<=\s)[1-9A-HJ-NP-Za-km-z]{32,44}(?=$|[\s.,])|(?<=\s)\$[A-Z]+(?=$|[\s.,])|(?<=^)\$[A-Z]+(?=$|[\s.,])"
pattern = re.compile(pattern_)
ticker_ca = {}

def get_cas(tweet):
    """retrieves the cas """
    matches = list(set(re.findall(pattern, tweet)))
    token_ca = []
    for i in range(len(matches)):
        match = matches[i]
        if match[0] == "$":
            if ticker_ca.get(match):
                #matches[i] = ticker_ca.get(match)
                token_ca.append((match, ticker_ca.get(match)))
            else:
                ca = get_ca(match)
                #matches[i] = ca
                token_ca.append((match, ca))
                ticker_ca[match] = ca
        else:
            found = 0
            for key, value in ticker_ca.items():
                if value == match:
                    token_ca.append((key, value))
                    found = 1
                    break
            if not found:
                ticker = get_name(match)
                token_ca.append((ticker, match))
                ticker_ca[ticker] = match
    return token_ca


def tweet_manu(username, tweet):
    """manupulates the tweet"""
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    date_str = tweet["created_at"]
    parsed_date = datetime.datetime.strptime(date_str, date_format)
    date = parsed_date.astimezone(pytz.utc)
    cas = get_cas(tweet["text"]) #[(ticker, ca), (ticker, ca)]
    for ca_ in cas:
        ticker = ca_[0]
        ca = ca_[1]
        if not ca or not ticker:
            continue
        try:
            start = (date - timedelta(minutes=5)).timestamp()
            end = (date + timedelta(minutes=15)).timestamp()
            prices = get_prices(ca, start, end)
            if not prices:
                continue
            add_doc(username, date, prices[0], prices[1], prices[2], prices[3], ca, ticker)
        except Exception as e:
            print(f'tweet_manu_error->{e}')


def posts(username, days):
    """retrieves tweet"""
    user_id = get_user_id(username)
    if user_id:
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
        

        if res_posts.status_code != 200:
            return posts
        print(posts)
        while 1:
            tweets = posts["data"]
            for tweet in tweets:
                tweet_manu(username, tweet)
            data_ = print_pretty()
            if posts["meta"].get("next_token"):
                params["pagination_token"] = posts["meta"]["next_token"]
                res_posts = requests.get(posts_url, headers=headers, params=params)
                posts = res_posts.json()
                if res_posts.status_code != 200:
                    print(posts)
                    break
            else:
                break
        return print_pretty()
