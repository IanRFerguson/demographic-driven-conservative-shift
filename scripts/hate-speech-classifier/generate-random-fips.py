#!/bin/python3

"""
About this Script

This is a simple, non-modular script to randomly pick
FIPS codes out of each racial change bin. We'll use these
later to generate Place IDs from Twitter's API

Ian Richard Ferguson | Stanford University
"""


# ---- Imports
import random, json
import pandas as pd


# ---- Run script
data = pd.read_csv('../../data/demographic-data/tidy-population-changes.csv').iloc[:, 1:]


def factor_levels(x):
    """
    Reformats group levels into menaingful factors
    """
    
    # If factor level isn't [1,2,3] return a missing value
    try:
        int(x)
    except:
        return 'MISSING'
    
    if int(x) == 1:
        return 'low'
    elif int(x) == 2:
        return 'mid'
    elif int(x) == 3:
        return 'high'
    else:
        return 'MISSING'
    
    
def valid_FIPS(x):
    """
    Pads FIPS level with a leading 0 if it's missing

    E.g., 1234 => 01234
    """
    
    if len(str(x)) == 5:
        return str(x)
    else:
        return f"0{x}"
    

for var in ['hispanic_change_bin', 'nhw_change_bin']:
   
    # Convert [1,2,3] to ['low','mid','high']
    data[var] = data[var].apply(lambda x: factor_levels(x))

# Pad FIPS codes with leading 0    
data['fips'] = data['fips'].apply(lambda x: valid_FIPS(x))

# Container for each factor level    
fips_codes_to_scrape = {'high-hispanic-change': [],
                       'mid-hispanic-change': [],
                       'low-hispanic-change':[]}

for rank in ['high','mid','low']:

    # Isolate rows for each change bin   
    temp = data[data['hispanic_change_bin'] == rank].reset_index(drop=True)
    
    # Randomly select 100 FIPS codes
    fips_codes = random.choices(temp['fips'], k=100)
    
    # Add list to container
    fips_codes_to_scrape[f'{rank}-hispanic-change'].extend(fips_codes)
    

# Push container to local JSON file    
with open('../../data/tweet-data/fips-codes-to-scrape.json', 'w') as outgoing:
    json.dump(fips_codes_to_scrape, outgoing, indent=4)

# Notify end user
print('\nJSON file saved - happy scraping!')