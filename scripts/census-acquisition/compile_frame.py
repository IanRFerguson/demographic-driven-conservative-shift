#!/bin/python3

"""
About this Script

* Converts state abbreviation to long-form (VA - Virginia)
* Reads in DW scores for all elected lawmakers from each state
* Assigns vector to DataFrame

Ian Ferguson | Stanford University
"""

# ----- Imports
import os, warnings, json
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from tqdm import tqdm

# ----- Functions
def load_frames():
      """
      Loads lawmaker data, state demo data, and state names JSON
      """

      data_dir = os.path.join('../../data')
      ideo = pd.read_csv(os.path.join(data_dir, 'lawmaker-subset-106-117.csv'))
      states = pd.read_csv(os.path.join(data_dir, 'state-demographics.csv'))

      with open('./states.json') as incoming:
            s_data = json.load(incoming)

      return ideo, states, s_data


def longform_state_id(X, STATE_DICT):
      """
      X => Incoming value from lambda function
      STATE_DICT => Dictionary with state names and abbreviations

      Converts abbreviation to longform state (VA - Virginia)
      """

      for key, value in STATE_DICT.items():
            if X == value:
                  return key


def dw_to_vector(DATA, STATE, SESSION):
      """
      DATA => Ideological data 
      STATE => State of interest (e.g., Virginia)
      SESSION => Session of interest (e.g., 112)

      Returns a list of lawmaker ideology scores for the given state and session
      """

      data = DATA[(DATA['state'] == STATE) & (DATA['congress'] == SESSION)].reset_index(drop=True)

      if len(data) == 0:
            return []

      return list(data['nominate_dim1'])


def main():
      # Read in data containers
      ideo, demo, states = load_frames()

      # Changes abbreviation to state name 
      ideo['state'] = ideo['state_abbrev'].apply(lambda x: longform_state_id(x, states))
      frames = []

      for year, session in zip([2000, 2010, 2020], [106, 111, 117]):
            # Subset demographics data by year
            temp = demo[demo['year'] == year].reset_index(drop=True)

            # Create new vector column
            temp['ideo_vector'] = temp['state'].apply(lambda x: dw_to_vector(ideo, x, session))

            # Add dataframe to container
            frames.append(temp)

      # Combine dataframes
      master = pd.concat(frames).sort_values(by='state')

      # Create average ideology column per year/state/session
      master['ideo_mean'] = master['ideo_vector'].apply(lambda x: np.mean(x))

      # Save CSV locally
      master.to_csv('../../data/state-ideo-data.csv', index=False)

      print('\nSaved to data directory')


if __name__ == "__main__":
      main()