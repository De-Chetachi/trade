#!/usr/bin/env python3
from pymongo import MongoClient

mongo_url = "mongodb+srv://chetagod4life:5E9U3D1IjXvJ7ZHh@cluster0.6tcnp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def get_db():
    """returns a mongodb database"""
    client = MongoClient(mongo_url)
    return client['price_action']
