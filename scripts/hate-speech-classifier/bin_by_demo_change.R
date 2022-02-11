# Goal of this Script
# Break distribution of white population % change in 3 groups
# We'll use these to identify geographic areas to target on Twitter
#
# Ian Richard Ferguson | Stanford University

# ---- Imports
library(tidyverse)
library(mltools)
library(usmap)

here <- "~/Box Sync/Research/Ian/DEMOGRAPHICS/conservatism-demographics/"
setwd(here)

# Read in Census Data
census.data <- read.csv('./data/demographic-data/county-demographics.csv')

# ---- Data cleaning
census.data <- census.data %>% 
        # Drop extraneous columns
        select(!c(year.1, white_pop)) %>% 
        
        # Years 2000 and 2020 only ... 20 year delta
        filter(year %in% c(2000, 2020)) %>% 
        mutate(
                # Make sure all FIPS codes are five-digits (leading 0)
                fips = str_pad(fips, 5, "left", 0),
                
                # Non-Hispanic White Population %
                nhw_population_pct = (non_hispanic_pop / total_pop),
               
                # Hispanic Population %
                hispanic_population_pct = (hispanic_pop / total_pop))


# Pivot data long => wide
census.wide <- census.data %>% 
        
        # E.g., total_pop => c(total_pop_2000, total_pop_2020)
        pivot_wider(c(state_name, county_name, fips), names_from = year,
                    values_from = c(total_pop, nhw_population_pct, hispanic_population_pct)) %>% 
        
        mutate(
                # Calculate population % change
                total_population_change = (total_pop_2020 - total_pop_2000) / total_pop_2000 * 100,
               
                # Hispanic population % change
                hispanic_population_change = (hispanic_population_pct_2020 - hispanic_population_pct_2000) / hispanic_population_pct_2000 * 100,
               
                # Non-Hispanic White population % change
                nhw_population_change = (nhw_population_pct_2020 - nhw_population_pct_2000) / nhw_population_pct_2000 * 100,
               
                # Scale all population % change observations
                total_pop_scaled = scale(total_population_change),
               
                # Scale all Hispanic % change observations
                hispanic_pop_scaled = scale(hispanic_population_change),
               
                # Scale all Non-Hispanic White % change observations
                nhw_pop_scaled = scale(nhw_population_change),
               
                # Break Hispanic % changes into three equal-sized groups
                hispanic_change_bin = as.factor(ggplot2::cut_number(hispanic_population_change, 3, labels=FALSE)),
               
                # Break Non-Hispanic White % changes into three equal-sized groups
                nhw_change_bin = as.factor(ggplot2::cut_number(nhw_population_change, 3, labels=FALSE)))


# Define custom color palette
my_colors <- c("#00798c", "#d1495b", "#edae49", "#66a182", "#2e4057", "#8d96a3", "#000000")

# ---- Plotting

# -- Raw
census.wide %>% 
        ggplot(aes(x = hispanic_population_change)) +
        geom_histogram(color='white', fill = my_colors[2]) +
        theme_minimal() +
        labs(x = "Population % Change", y = "n",
             title = "Hispanic Population Changes",
             subtitle = "2000 to 2020") +
        theme(plot.title = element_text(hjust = 0.5, face='bold'),
              plot.subtitle = element_text(hjust = 0.5))

plot_usmap(data = census.wide, regions = 'county', values = 'hispanic_population_change', 
           exclude = c('HI', 'AK'), color = 'black') +
        labs(title = 'Hispanic Population % Change',
             subtitle = '2000 to 2020', fill = '') +
        theme(plot.title = element_text(hjust = 0.5, face='bold'),
              plot.subtitle = element_text(hjust = 0.5),
              legend.position = "bottom") +
        scale_fill_continuous(low = 'white', high = my_colors[2])


# -- Binned
census.wide %>% 
        ggplot(aes(x = hispanic_population_change, fill = hispanic_change_bin)) +
        geom_histogram(color='white') +
        theme_minimal() +
        scale_fill_manual(labels = c('Low', 'Med', 'High'), values = my_colors) +
        labs(x = "Population % Change", y = "n",
             fill = "", title = "Hispanic Population % Change",
             subtitle = "2000 to 2020") +
        theme(plot.title = element_text(hjust = 0.5, face='bold'),
              plot.subtitle = element_text(hjust = 0.5))

plot_usmap(data = census.wide, regions = 'county', values = 'hispanic_change_bin', 
           exclude = c('HI', 'AK'), color = 'black') +
        labs(title = 'Binned Deltas - Hispanic Population % Change',
             subtitle = '2000 to 2020', fill = '') +
        theme(plot.title = element_text(hjust = 0.5, face='bold'),
              plot.subtitle = element_text(hjust = 0.5),
              legend.position = 'bottom') +
        scale_fill_manual(values = my_colors, labels = c('Low', 'Med', 'High'))

plot_usmap(data = census.wide, regions = 'county', values = '')

census.wide %>% 
        arrange(desc(hispanic_population_change)) %>% 
        filter(state_name == ' Georgia') %>% 
        select(state_name, county_name, hispanic_population_change) %>% head()

plot_usmap(data = census.wide, regions = 'county', values = 'hispanic_population_change',
           include=c('GA'), color = 'black') +
        scale_fill_continuous(type = 'viridis') +
        labs(fill = '', title = 'Hispanic Population % Deltas',
             subtitle = '2000 to 2020') +
        theme(plot.title = element_text(hjust = 0.5, face = 'bold'),
              plot.subtitle = element_text(hjust = 0.5))

plot_usmap(data = census.wide, regions = 'county', values = 'nhw_population_change',
           include=c('GA'), color = 'black') +
        scale_fill_continuous(type = 'viridis') +
        labs(fill = '', title = 'Non-Hispanic White Population % Deltas',
             subtitle = '2000 to 2020') +
        theme(plot.title = element_text(hjust = 0.5, face = 'bold'),
              plot.subtitle = element_text(hjust = 0.5))

# Write DataFrame to local CSV
#write.csv(census.wide, file = './data/demographic-data/tidy-population-changes.csv', fileEncoding = 'utf-8')