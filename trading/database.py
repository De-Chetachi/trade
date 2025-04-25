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
        sys.exit()
    try:
        client = MongoClient(mongo_url)
        db = client['price_action']
        return db
    except Exception as e:
        print("mongo connection error")
        sys.exit()
