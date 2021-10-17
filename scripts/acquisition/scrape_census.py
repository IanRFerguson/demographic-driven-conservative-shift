#!/bin/python3

"""
NOTE: You need a valid Census.gov API key to run this script

About this Script

* Downloads state-wise racial demographic information from 2010 and 2020
* Compiles resulting data in a DataFrame, with two rows per state (one / year)

Ian Ferguson | Stanford University
"""

# ----- Imports
import os, requests, json, warnings, sys
warnings.filterwarnings('ignore')

import pandas as pd
from tqdm import tqdm


# ----- Functions
def load_API():
      """
      Reads in API key (txt) and year-wise API parameters (JSON)
      """

      for file in ['SECRET_api-key.txt', 'api_call.json']:
            # Confirm that both relevant files exist
            temp = os.path.join('.', file)

            if not os.path.exists(temp):
                  raise OSError(f'Looks like {file} does not exist...')

      with open('./SECRET_api-key.txt') as incoming:
            key = incoming.read().replace('\n', '')

      with open('./api_call.json') as incoming:
            call = json.load(incoming)

      # Make sure the number of parameters per year are equivalent
      test_len = len(call[list(call.keys())[0]])

      for k in ['2000', '2010', '2020']:
            if len(call[k]) != test_len:
                  raise ValueError(f'Length mismatch in API call @ {k}')

      return key, call


def format_call(API_KEY, YEAR, API_DATA, ROI):
      """
      API_KEY => Valid key from Census.gov
      YEAR => 2000, 2010, 2020
      API_DATA => Dictionary object
      ROI => Region of interest, STATE or COUNTY

      This function creates a complete API call
      """

      base_url = API_DATA[YEAR]['url'][ROI]
      vars = ",".join(API_DATA[YEAR]['census-vars'])
      
      return base_url.format(vars, API_KEY)


def scrape_census(API_KEY, YEAR, API_DATA, ROI):
      """
      API_KEY => Valid key from Census.gov
      YEAR => 2000, 2010, 2020
      API_DATA => Dictionary object
      ROI => State or County, level of interest
      """

      # Structure API call
      call = format_call(API_KEY=API_KEY, YEAR=YEAR, API_DATA=API_DATA, ROI=ROI)
      
      # Pull data into variable
      r = requests.get(call)

      # Read JSON information from obtained data
      data = r.json()

      # Push data to DataFrame object
      frame = pd.DataFrame(data[1:], columns=data[0])

      # Reassign column names
      clean_vars = API_DATA['master'][ROI]
      frame.columns = clean_vars
      
      return frame


def cleanup_county_data(DF):
      """
      DF => Pandas DataFrame object

      This function performs the following
            * Compiles FIPS code
      """

      new_order = ["year", "county_state", "total_pop",
                   "white_pop", "total_pop2",
                   "non_hispanic_pop", "hispanic_pop",
                   "non_hispanic_white_pop",
                   "state_code", "county_code"]

      try:
            DF = DF[new_order]
      except Exception as e:
            raise ValueError(f"\nack! {e}")

      DF['county_name'] = DF['county_state'].apply(lambda x: x.split(',')[0])
      DF['state_name'] = DF['county_state'].apply(lambda x: x.split(',')[1])

      def get_fips(DF):
            state = DF['state_code']
            county = DF['county_code']

            return f"{state}{county}"

      DF['fips'] = DF.apply(get_fips, axis=1)
      to_drop = ['county_state', 'state_code', 'county_code', 'total_pop2']
      DF = DF.drop(columns=to_drop)

      new_order = ['year', 'state_name', 'county_name', 'fips'] + list(DF.columns[:5])
      return DF[new_order].sort_values(by='state_name').reset_index(drop=True)


def main():
      try:
            roi = sys.argv[1].lower()
      except:
            raise OSError("\nack! missing command line argument - call STATE or COUNTY")

      # Instantiate API key and request parameters
      key, call = load_API()

      # Empty list to append into
      frames = []

      for year in tqdm(['2000', '2010', '2020']):
            temp = scrape_census(key, year, call, roi)
            temp['year'] = [year] * len(temp)
            frames.append(temp)

      # Stack dataframes into one object and save locally
      if roi.lower() == "state":
            master = pd.concat(frames).sort_values(by='state')

      elif roi.lower() == "county":
            master = pd.concat(frames).sort_values(by='county_state')
            master = cleanup_county_data(master)

      master.to_csv(f'../../data/{roi.lower()}-demographics.csv', index=False)


if __name__ == "__main__":
      main()