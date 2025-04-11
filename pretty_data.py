#!/usr/bin/env python3

from collection import items
from pandas import DataFrame
def print_pretty():
    """prints the inflencer price action in a pretty way"""
    items_df = DataFrame(items())
    print(items_df)
