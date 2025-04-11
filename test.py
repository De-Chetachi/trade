#!/usr/bin/env python3

import requests
import sys
import datetime
import pytz
from datetime import timedelta
import re


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
        "created_at": "Wed Apr 06 18:40:40 +0000 2025",
        "id": "1346889436626259968",
        "text": "Learn $solana how to use the user Tweet timeline and user mention timeline endpoints in the X API v2 to explore Tweet\\u2026 https:\\/\\/t.co\\/56a0vZUx7i",
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

days_cap = 7
tweet_objects = data["includes"]["tweets"]

tweets = [twee["text"] for twee in tweet_objects] #this is a list of just tweets without metadata

#next we need the tweets based on the date of creation so
#if the given parameter is 30days cap we need to find tweets from the last 30 dyas
# "created_at": "Wed Jan 06 18:40:40 +0000 2021",

compare_date = datetime.datetime.now() - timedelta(days=days_cap)
date_format = "%a %b %d %H:%M:%S %z %Y"


cmc_key = "4002cfa0-5c71-43e4-b1db-c0a09693d0c4"
coin = "$solana"
for tweet in tweet_objects:
    date_str = tweet["created_at"]
    parsed_date = datetime.datetime.strptime(date_str, date_format)
    print(parsed_date)
    utc_date = parsed_date.astimezone(pytz.utc)
    utc_string = utc_date.strftime("%Y-%m-%d %H:%M:%S UTC")
    date = datetime.datetime.strptime(utc_string, "%Y-%m-%d %H:%M:%S UTC")
    if date >= compare_date:
        text = tweet["text"]

        pattern = re.compile(re.escape(coin), re.IGNORECASE)
        match = pattern.search(text)
        if match:
            print(text)



#r.json()
