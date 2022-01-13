#!/bin/python3

"""
About this Script

Using our geodata.csv file, we'll loop through each
identified Place ID and scrape n tweets from it

Ian Richard Ferguson | Stanford University
"""


# ---- Imports
import tweepy, json, os
import pandas as pd
from tqdm import tqdm
from sklearn.utils import shuffle


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


def scraper(api, count, fips, place_id, demographic_status):
    """
    api => Validated tweepy.API object
    count => Number of tweets you want to pull
    fips => Five-digit FIPS code, used for identification at this stage
    geocode => [longitude, latitude]
    demographic_status => [high, mid, low]

    Returns Pandas DataFrame
    """
    
    place = f"place:{place_id}"

    # Empty lists to push scraped Twitter data into
    created, name, screen_name, location, text, likes, rts = [], [], [], [], [], [], []

    # Original context is best for our purposes
    query_target = place + " -filter:retweets -filter:links"

    # Loop through each identified tweet and push it to a list
    for tweet in tweepy.Cursor(api.search,
                               q = query_target,
                               lang = 'en',
                               tweet_mode = 'extended',
                               result_type = 'recent').items(count):

        created.append(tweet.created_at)
        name.append(tweet.user.name)
        screen_name.append(tweet.user.screen_name)
        location.append(tweet.user.location)
        text.append(tweet.full_text)
        likes.append(tweet.favorite_count)
        rts.append(tweet.retweet_count)

    # Organize tweet data into a Pandas DataFrame
    tweet_data = pd.DataFrame({'DateTime': created,
                         'UserName': name,
                         'ScreenName': screen_name,
                         'Location': location,
                         'Tweet': text,
                         'Likes': likes,
                         'Retweets': rts})
    
    tweet_data['fips'] = [fips] * len(tweet_data)
    tweet_data['hispanic-pop-change'] = [demographic_status] * len(tweet_data)
    tweet_data['place_id'] = [place_id] * len(tweet_data)

    return tweet_data


def main():

    # Validate credentials and instantiate API object
    api = connect_to_API()

    # Read in CSV with identified place IDs
    geo_data = pd.read_csv('../../data/tweet-data/geodata.csv').iloc[:, 2:]

    geo_data = shuffle(geo_data).reset_index()

    # Parent DataFrame to append into
    output = pd.DataFrame()
    print('Tweets scraping...')

    for index, places in tqdm(enumerate(geo_data['places'])):

        # Clean up individual place value, cast to list
        places = [x.replace('[', '').replace(']', '').replace('\'', '').strip() for x in places.split(',')]

        # Isolate FIPS code and dem status for each row in CSV
        fips, dem_status = geo_data['fips'][index], geo_data['hispanic-pop-change'][index]

        for place in places:

            # Scrape tweets and store as temporary DataFrame
            temp = scraper(api=api, count=500, fips=fips, place_id=place, demographic_status=dem_status)

            # Append to parent DataFrame
            output = output.append(temp, ignore_index=True)

    # Push to local CSV
    output.to_csv('../../data/tweet-data/all-tweets-scraped.csv')
    print('\nTweets have been scraped and saved locally')


# ---- Run script
if __name__ == "__main__":
    main()