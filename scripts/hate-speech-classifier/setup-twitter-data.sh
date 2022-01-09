#!/bin/bash

# ---- About this script
# This shell script wraps various R and Python
# scripts developed to support this research program
#
# Ian Richard Ferguson | Stanford University

base_dir="/Users/Ian/Box Sync/Research/Ian/DEMOGRAPHICS/conservatism-demographics"
data_output="${base_dir}/data/tweet-data"
working_directory="${base_dir}/scripts/hate-speech-classifier"

mkdir -p $data_output
cd $working_directory

Rscript bin-by-demo-change.R                                # Creates aggregate demographic change CSV
python3 generate-random-fips.py                             # Isolate random FIPS codes / bin
python3 generate geo-data.py                                # Combine FIPS, dem status, longitude and latitude
python3 generate-place-ids.py                               # Find Twitter place IDs to scrape at geo level