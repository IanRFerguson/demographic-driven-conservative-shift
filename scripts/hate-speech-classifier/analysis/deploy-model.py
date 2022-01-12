#!/bin/python3

"""
About this Script

We'll apply our trained hate speech classifier to our
corpus of novel tweets

Ian Richard Ferguson | Stanford University
"""


# ---- Imports
import re, pickle
import pandas as pd


# ---- Helpers
def is_mention(x):
      """
      Identifies if a tweet is in response to another Twitter user

      Returns a binary value
      """

      if str(x)[0] == "@":
            return 1
      else:
            return 0


def clean_text_data(DF, VAR):
      """
      DF => Pandas DataFrame object
      VAR => Feature (column in DataFrame) containing text data

      Strips extraneous text characters from Tweet text

      Returns full DataFrame
      """

      # Transposes all text to lowercase
      DF[VAR] = DF[VAR].str.lower()

      # Remove extraneous characters from Tweet body
      DF[VAR] = DF[VAR].apply(lambda x: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", x))

      # Remove all whitespace
      DF[VAR] = DF[VAR].str.strip()

      return DF


def main():
      
      # Read in Tweets in DataFrame object
      tweets = pd.read_csv('../../../data/tweet-data/all-tweets-scraped.csv').iloc[:, 1:]

      # Denotes if Tweet is in reference to another Twitter user
      tweets['is_mention'] = tweets['Tweet'].apply(lambda x: is_mention(x))

      # Clean Tweet text
      tweets = clean_text_data(tweets, 'Tweet')

      # Load trained Hate Speech classifier
      with open('../../../data/tweet-data/trained_hs_classifier.sav', 'rb') as incoming:
            classifier = pickle.load(incoming)

      # Apply classifier to Tweet data
      tweets['predicted-hs'] = classifier.predict(tweets['Tweet'])

      # Save locally
      tweets.to_csv('../../../data/tweet-data/all-tweets-scraped.csv')


# ---- Run script

if __name__ == "__main__":
      main()
