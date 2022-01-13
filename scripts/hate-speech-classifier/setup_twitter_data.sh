#!/bin/bash

# ---- About this script
# This shell script wraps various R and Python
# scripts developed to support this research program
#
# Ian Richard Ferguson | Stanford University

base_dir="../.."
data_output="${base_dir}/data/tweet-data"
working_directory="${base_dir}/scripts/hate-speech-classifier"

mkdir -p $data_output
cd $working_directory

pwd

Rscript bin_by_demo_change.R                                # Creates aggregate demographic change CSV
python3 generate_random_fips.py                             # Isolate random FIPS codes / bin
python3 generate_geo_data.py                                # Combine FIPS, dem status, longitude and latitude
python3 generate_place_ids.py                               # Find Twitter place IDs to scrape at geo level