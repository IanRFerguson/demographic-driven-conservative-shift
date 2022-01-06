#!/bin/python3

"""

"""


# ---- Imports
import tweepy, json, os
import pandas as pd


# ---- Helper functions
def connect_to_API():
    """
    
    """

    with open('./credentials.json') as incoming:
        creds = json.load(incoming)

    auth_set = tweepy.OAuthHandler(consumer_key='',
                                consumer_secret='')

    auth_set.set_access_token(key='',
                            secret='')

    api = tweepy.API(auth_set, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
    except Exception as e:
        raise ValueError(e)

    return api


def scrape_tweets(geocode):
    """
    geocode =>

    Returns Pandas DataFrame of scraped tweets
    """

    pass


def main():
    """
    
    """

    pass


# ---- Run script
if __name__ == "__main__":
    main()