# Goal of this Script
# Break distribution of white population % change in 3 groups
# We'll use these to identify geographic areas to target on Twitter

# ---- Imports
library(tidyverse)
library(mltools)
library(usmap)

here <- "~/Box Sync/Research/Ian/DEMOGRAPHICS/conservatism-demographics/"
setwd(here)

census.data <- read.csv('./data/demographic-data/county-demographics.csv')

# ---- Data cleaning
census.data <- census.data %>% 
        select(!c(year.1, white_pop)) %>% 
        filter(year %in% c(2000, 2020)) %>% 
        mutate(fips = str_pad(fips, 5, "left", 0),
               nhw_population_pct = (non_hispanic_pop / total_pop),
               hispanic_population_pct = (hispanic_pop / total_pop))

census.wide <- census.data %>% 
        pivot_wider(c(state_name, county_name, fips), names_from = year,
                    values_from = c(total_pop, nhw_population_pct, hispanic_population_pct)) %>% 
        
        mutate(total_population_change = (total_pop_2020 - total_pop_2000) / total_pop_2000 * 100,
               hispanic_population_change = (hispanic_population_pct_2020 - hispanic_population_pct_2000) / hispanic_population_pct_2000 * 100,
               nhw_population_change = (nhw_population_pct_2020 - nhw_population_pct_2000) / nhw_population_pct_2000 * 100,
               
               total_pop_scaled = scale(total_population_change),
               hispanic_pop_scaled = scale(hispanic_population_change),
               nhw_pop_scaled = scale(nhw_population_change),
               
               hispanic_change_bin = as.factor(ggplot2::cut_number(hispanic_population_change, 3, labels=FALSE)),
               nhw_change_bin = as.factor(ggplot2::cut_number(nhw_population_change, 3, labels=FALSE)))


# ---- Hispanic
census.wide %>% 
        ggplot(aes(x = hispanic_population_change, fill = hispanic_change_bin)) +
        geom_histogram(color='white') +
        theme_minimal()


# ---- Non-Hispanic White
census.wide %>% 
        ggplot(aes(x = nhw_population_change, fill=nhw_change_bin)) +
        geom_histogram(color='white', position = "dodge") +
        theme_minimal()

write.csv(census.wide, file = './data/demographic-data/tidy-population-changes.csv', fileEncoding = 'utf-8')
