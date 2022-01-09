#!/bin/python3

"""
With our list of random FIPS codes per demographic
bin, we'll want to isolate the longitude and latitude
in a tidy DataFrame object

Ian Richard Ferguson | Stanford University
"""

# ---- Imports
import pandas as pd
import json


# ---- Run script
with open('../../data/tweet-data/fips-codes-to-scrape.json') as incoming:
    
    # Read in FIPS codes as a dictionary object
    data = json.load(incoming)
    
# Read in County Centers CSV (with long/lat coordinates)
county_centers = pd.read_csv('https://raw.githubusercontent.com/btskinner/spatial/master/data/county_centers.csv')


def valid_FIPS(x):
    """
    Some of our FIPS values don't have a leading 0
    This function fixes that issue
    """

    temp = str(x)
    
    # E.g., 12345
    if len(temp) == 5:
        return temp
    
    # 1234 => 01234
    else:
        return f"0{temp}"

# Pad incomplete FIPS values
county_centers['fips'] = county_centers['fips'].apply(lambda x: valid_FIPS(x))

# Isolate longitude and latitude coordinates
county_centers = county_centers.loc[:, ['fips', 'clon10', 'clat10']]

# Instantiate new DataFrame to store our geodata
output = pd.DataFrame(columns=['fips', 'hispanic-pop-change'])

# Loop through high/mid/low demographic change values
for key in list(data.keys()):
    temp = pd.DataFrame(data[key], columns=['fips'])
    temp['hispanic-pop-change'] = [key.split('-')[0]] * len(temp)
    
    # Append new data to aggregate DataFrame
    output = output.append(temp, ignore_index=True)


# Merge with geo coordinates per FIPS code
output = output.merge(county_centers, on='fips')

# Save to local CSV
output.to_csv('../../data/tweet-data/geodata.csv')
print('\nGeodata saved in tweet-data subfolder')