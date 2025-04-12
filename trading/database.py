#!/usr/bin/env python3
from pymongo import MongoClient
import os
import sys

key = "MONGO_URL"
mongo_url = os.environ.get(key)

def get_db():
    """returns a mongodb database"""
    if not mongo_url:
        print('provide mongo_url env variable')
        return
    try:
        client = MongoClient(mongo_url)
        return client['price_action']
    except Exception as e:
        print("mongo connectio error")
        sys.exit()
