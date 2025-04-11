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

#username = sys.argv[1]
#print(username)
username = "test"
coin = sys.argv[1]
ticker = sys.argv[2]
days_cap = int(sys.argv[3])
#token = ""
#bearer = f"Bearer {token}"
#headers = {"Authorization": bearer, "Content-Type": "application/json"}


#url = f"https://api.twitter.com/2/users/:id" based on id
url = f"https://api.twitter.com/2/users/by/username/{username}"
#r = requests.get( url, headers=headers)
#data = r.json();
data =  {
  "data": {
    "created_at": "2013-12-14T04:35:55Z",
    "id": "2244994945",
    "name": "X Dev",
    "protected": False,
    "username": "TwitterDev"
  },
  "errors": [
    {
      "detail": "<string>",
      "status": 123,
      "title": "<string>",
      "type": "<string>"
    }
  ],
  "includes": {
    "media": [
      {
        "height": 1,
        "media_key": "<string>",
        "type": "<string>",
        "width": 1
      }
    ],
    "places": [
      {
        "contained_within": [
          "f7eb2fa2fea288b1"
        ],
        "country": "United States",
        "country_code": "US",
        "full_name": "Lakewood, CO",
        "geo": {
          "bbox": [
            -105.193475,
            39.60973,
            -105.053164,
            39.761974
          ],
          "geometry": {
            "coordinates": [
              -105.18816086351444,
              40.247749999999996
            ],
            "type": "Point"
          },
          "properties": {},
          "type": "Feature"
        },
        "id": "f7eb2fa2fea288b1",
        "name": "Lakewood",
        "place_type": "city"
      }
    ],
    "polls": [
      {
        "duration_minutes": 5042,
        "end_datetime": "2023-11-07T05:31:56Z",
        "id": "1365059861688410112",
        "options": [
          {
            "label": "<string>",
            "position": 123,
            "votes": 123
          }
        ],
        "voting_status": "open"
      }
    ],
    "topics": [
      {
        "description": "All about technology",
        "id": "<string>",
        "name": "Technology"
      }
    ],
    "tweets": [
      {
        "author_id": "2244994945",
        "created_at": "Wed Jan 06 18:40:40 +0000 2021",
        "id": "1346889436626259968",
        "text": "Learn how to use the user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet\\u2026 https:\\/\\/t.co\\/56a0vZUx7i",
        "username": "XDevelopers"
      },

      {
        "author_id": "2244994945",
        "created_at": "Wed Jan 06 18:40:40 +0000 2021",
        "id": "1346889436626259968",
        "text": "Learn how to use the user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet\\u2026 https:\\/\\/t.co\\/56a0vZUx7i",
        "username": "XDevelopers"
      },

      {
        "author_id": "2244994945",
        "created_at": "Wed Apr 11 10:40:40 +0000 2025",
        "id": "1346889436626259968",
        "text": "Learn how to use the  user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet\\u2026 https:\\/\\/t.co\\/56a0vZUx7i",
        "username": "XDevelopers"
      },

      {
        "author_id": "2244994945",
        "created_at": "Wed Apr 11 10:40:40 +0000 2025",
        "id": "1346889436626259968",
        "text": "Learn how to use the user Tweet $PEPE timeline and user mention timeline endpoints in the X API v2 to explore Tweet\\u2026 https:\\/\\/t.co\\/56a0vZUx7i",
        "username": "XDevelopers"
      },

      {
        "author_id": "2244994945",
        "created_at": "Wed Apr 11 10:40:40 +0000 2025",
        "id": "1346889436626259968",
        "text": "Learn  how to use the user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet\\u2026 https:\\/\\/t.co\\/56a0vZUx7i",
        "username": "XDevelopers"
      }
    ],
    "users": [
      {
        "created_at": "2013-12-14T04:35:55Z",
        "id": "2244994945",
        "name": "X Dev",
        "protected": False,
        "username": "TwitterDev"
      }
    ]
  }
}

tweets = data["includes"]["tweets"]
#this returns a list of tweets each has a couple of keys
# we are interested in the id, text, created_at

#tweets = [twee["text"] for twee in tweet_objects] #this is a list of just tweets without metadata

#next we need the tweets based on the date of creation so
#if the given parameter is 30days cap we need to find tweets from the last 30 dyas 
# "created_at": "Wed Jan 06 18:40:40 +0000 2021",

compare_date = datetime.datetime.now(pytz.utc) - timedelta(days=days_cap)

date_format = "%a %b %d %H:%M:%S %z %Y"


for tweet in tweets:
    date_str = tweet["created_at"]
    parsed_date = datetime.datetime.strptime(date_str, date_format)
    date = parsed_date.astimezone(pytz.utc)

    if date < (datetime.datetime.now(pytz.utc) - timedelta(days=1)):
            print("this tweet is skipped cause it was made more that 24 hours ago")
            continue
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

            except Exception as e:
                print(e)

print_pretty()
