#!/bin/python3

"""
NOTE: You need a valid Census.gov API key to run this script

About this Script

* Downloads state-wise racial demographic information from 2010 and 2020
* Compiles resulting data in a DataFrame, with two rows per state (one / year)

Ian Ferguson | Stanford University
"""

# ----- Imports
import os, requests, json, warnings
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


def format_call(API_KEY, YEAR, API_DATA):
      """
      API_KEY => Valid key from Census.gov
      YEAR => 2000, 2010, 2020
      API_DATA => Dictionary object

      This function creates a complete API call
      """

      base_url = API_DATA[YEAR]['url']
      vars = ",".join(API_DATA[YEAR]['census-vars'])
      
      return base_url.format(vars, API_KEY)


def scrape_census(API_KEY, YEAR, API_DATA):
      """
      API_KEY => Valid key from Census.gov
      YEAR => 2000, 2010, 2020
      API_DATA => Dictionary object
      """

      # Structure API call
      call = format_call(API_KEY=API_KEY, YEAR=YEAR, API_DATA=API_DATA)
      
      # Pull data into variable
      r = requests.get(call)

      # Read JSON information from obtained data
      data = r.json()

      # Push data to DataFrame object
      frame = pd.DataFrame(data[1:], columns=data[0])

      # Reassign column names
      clean_vars = API_DATA['master']
      frame.columns = clean_vars
      
      return frame


def main():
      # Instantiate API key and request parameters
      key, call = load_API()

      # Empty list to append into
      frames = []

      for year in tqdm(['2000', '2010', '2020']):
            temp = scrape_census(key, year, call)
            temp['year'] = [year] * len(temp)
            frames.append(temp)

      # Stack dataframes into one object and save locally
      master = pd.concat(frames).sort_values(by='state')
      master.to_csv('../../data/state-demographics.csv', index=False)


if __name__ == "__main__":
      main()