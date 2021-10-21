# Template script to source from for FIPS-level analyses
# Ian Ferguson | Stanford University

# ----- Imports
library(tidyverse)
library(usmap)

here <- "~/Box Sync/Research/Ian/DEMOGRAPHICS/conservatism-demographics/"
setwd(here)


# ----- Data Carpentry

# Data scraped from the US Census API
census.data <-read.csv("./data/county/county-demographics.csv") %>% 
        select(-year.1) %>% 
        filter(year %in% c(2000, 2020)) %>%
        mutate(
                # Add leading 0 to FIPS codes that are too short
                fips = str_pad(fips, 5, "left", 0),
               
                # Calculate Hispanic and Non-Hispanic White population percentages
                hispanic.pop.pct = hispanic_pop / total_pop,
                nhw.pop.pct = non_hispanic_pop / total_pop)


# Pivot census data wider - one row / FIPS code
census.wide <- census.data %>% 
        pivot_wider(id_cols = c(state_name, county_name, fips),
                    names_from = year,
                    values_from = c(hispanic.pop.pct, nhw.pop.pct, total_pop))


# Data obtained via MIT's election lab
voting.data <- read.csv("./data/ideo/countypres_2000-2020.csv") %>% 
        select(-c(state_po, office, version, mode)) %>% 
        mutate(
                # Add leading 0 to FIPS codes that are too short
                fips = str_pad(county_fips, 5, side="left", pad=0),
               
                # Percentage of votes per FIPS code that each candidate received
                pct.raw = candidatevotes / totalvotes) %>% 
        select(-county_fips) %>% 
        filter(
                # Two party system ... no comment
                party %in% c("DEMOCRAT", "REPUBLICAN"),
                year %in% c(2000, 2020)) %>% 
        
        # Data contains extra rows for some localities ... we'll aggregate them using this stat
        group_by(fips, year, party) %>% 
        mutate(voting.percentage = sum(pct.raw)) %>% 
        slice(1) %>% 
        ungroup()

# Pivot voting data wider - One row per FIPS code
voting.wide <- voting.data %>% 
        pivot_wider(id_cols = fips,
                    names_from = c(party, year),
                    values_from = voting.percentage)

# Aggregate census and vote data, on FIPS code
all.data <- census.wide %>% left_join(voting.wide, by="fips") %>% 
        mutate(
                # Binary vote outcome per FIPS code
                outcome.2000 = ifelse(DEMOCRAT_2000 > REPUBLICAN_2000, "D", "R"),
                outcome.2020 = ifelse(DEMOCRAT_2020 > REPUBLICAN_2020, "D", "R"),
                
                # Identifies FIPS codes that flipped on party vote between 2000 and 2020
                vote.flipped = as.factor(ifelse(outcome.2020 != outcome.2000, 1, 0))) %>% 
        rename(
                # Abbreviate party name_year naming convention
                dem_2000 = DEMOCRAT_2000,
                dem_2020 = DEMOCRAT_2020,
                rep_2000 = REPUBLICAN_2000,
                rep_2020 = REPUBLICAN_2020)

# Remove extra DataFrames from environment - we'll export everything else
rm(census.data, census.wide, voting.data, voting.wide)