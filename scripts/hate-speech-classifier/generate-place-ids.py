#!/bin/python3

"""
About this Script

Tweepy allows us to conduct geographic searches based on a "Place" ...
Since we have the long-lat coordinates for our high/mid/low dem change
areas we can plug these into the api.reverse_geocde function to get a
list of place IDs for each long/lat area

Ian Richard Ferguson | Stanford University
"""


# ---- Imports
import os, random, json, tweepy
from tqdm import tqdm
import pandas as pd


# ---- Helpers
def connect_to_API():
      """
      Connect to Twitter's API via Tweepy

      Returns tweepy.API object
      """

      # Read in Twitter Developer credentials as a dictionary object
      with open('./credentials.json') as incoming:
            creds = json.load(incoming)

      # Impute crednetials in Auth Handler
      auth_set = tweepy.OAuthHandler(consumer_key=creds['API-KEY'],
                                     consumer_secret=creds['API-SECRET'])

      auth_set.set_access_token(key=creds['ACCESS'], secret=creds['SECRET'])

      # Instantiate API object
      api = tweepy.API(auth_set, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

      try:
            api.verify_credentials()
            print('\n** Valid credentials **\n')
      except Exception as e:
            raise e

      return api


def get_place_ids(DF, API):
      """
      DF => DataFrame object
      API =>

      This function runs through DataFrame and generates
      a maximum five (5) place IDs that we'll use to scrape
      geo-specific tweets
      """

      # Assign empty values to new column
      DF['places'] = [None] * len(DF)

      for index, val in tqdm(enumerate(DF['fips'])):

            # This list will hold our accumulated Place IDs per FIPS code
            container = []

            # Isolate longitude and latitude values
            long, lat = DF['clon10'][index], DF['clat10'][index]

            # Generate list of places associated with our long/lat coordinates
            places = API.reverse_geocode(lat, long)

            for place in places[:6]:

                  # US is too coarse
                  if place.name != 'United States':
                        container.append(place.id)
                  else:
                        continue

            # Assign list of Place IDs to DataFrame
            DF['places'][index] = container


# ---- Run script
def main():
      # Connect to Twitter API + instantiate connection object
      api = connect_to_API()

      # Read in local geodata CSV
      target_data = pd.read_csv('../../data/tweet-data/geodata.csv')

      # Apply helper function to isolate Place IDs
      get_place_ids(target_data, api)

      # Write DataFrame to local CSV
      target_data.to_csv('../../data/tweet-data/geodata.csv')
      print('\n ** Place IDs Saved **\n')


if __name__ == "__main__":
      main()