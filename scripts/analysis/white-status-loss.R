# White Status Loss Over Time
#
# This analysis will quantify changes in Hispanic and Non-Hispanic White population changes over time
# Ian Richard Ferguson | Stanford University

# ----- Imports
library(tidyverse)
library(usmap)

here <- "~/Box Sync/Research/Ian/DEMOGRAPHICS/conservatism-demographics/"
setwd(here)

# Read in ideology and demographic data derived from Python scripts
master <- read.csv(paste0(here, "data/state-ideo-data.csv")) %>% select(-total_pop2)

# New aggregate DataFrame (one row per state)
wsl <- master %>% 
        select(year, state, total_pop, hispanic_pop, non_hispanic_white_pop, ideo_mean) %>% 
        
        # Calculate population percentages
        mutate(nhw_pop_ct = non_hispanic_white_pop / total_pop,
               h_pop_ct = hispanic_pop / total_pop) %>% 
        
        # Widen DataFrame (one row:state)
        pivot_wider(id_cols = state, names_from = year, values_from = c(h_pop_ct, nhw_pop_ct, ideo_mean)) %>% 
        
        # Remove rows with no representation (Puerto Rico, DC)
        drop_na() %>% 
        
        # Calculate shifts in time (00.20 = change from 2020 to 2000)
        mutate( # Hispanic shifts
                h.shift.00.20 = (h_pop_ct_2020 - h_pop_ct_2000),
                h.shift.00.10 = (h_pop_ct_2010 - h_pop_ct_2000),
                h.shift.10.20 = (h_pop_ct_2020 - h_pop_ct_2010),
               
                # Non-Hispanic White shifts
                nhw.shift.00.20 = (nhw_pop_ct_2020 - nhw_pop_ct_2000),
                nhw.shift.00.10 = (nhw_pop_ct_2010 - nhw_pop_ct_2000),
                nhw.shift.10.20 = (nhw_pop_ct_2020 - nhw_pop_ct_2010),
                
                # Ideology shifts
                ideo.shift.00.20 = (ideo_mean_2020 - ideo_mean_2000),
                ideo.shift.00.10 = (ideo_mean_2010 - ideo_mean_2000),
                ideo.shift.10.20 = (ideo_mean_2020 - ideo_mean_2010))

# Custom mapping function
plot.temporal.map <- function(VAR, LOW, HIGH, TITLE, SUBTITLE="") {
        plot_usmap(data = wsl, values = VAR, regions = "states", color = "white") +
                scale_fill_continuous(low = LOW, high = HIGH, name = "") +
                labs(title = TITLE, subtitle = SUBTITLE) +
                theme(plot.title = element_text(hjust = 0.5, face = "bold"),
                      plot.subtitle = element_text(hjust = 0.5),
                      legend.position = "bottom")
}

# ------ Plotting Maps
# Hispanic Data
plot.temporal.map("h_pop_ct_2000", "grey", "red", "Hispanic Population % (2000")
plot.temporal.map("h_pop_ct_2020", "grey", "red", "Hispanic Population % (2020)")
plot.temporal.map("h.shift.00.20", "lightgrey", "red", "Hispanic Population % Change", "2000 to 2020")

# Non-Hispanic White Data
plot.temporal.map("nhw_pop_ct_2000", "white", "darkblue", "Non-Hispanic White Population % (2000)")
plot.temporal.map("nhw_pop_ct_2020", "white", "darkblue", "Non-Hispanic White Population % (2020)")
plot.temporal.map("nhw.shift.00.20", "red", "white", "Non-Hispanic White Population % Change", "2000 to 2020")

# Ideology
plot.temporal.map("ideo_mean_2000", "darkblue", "red", "Average DW Nom Scores (2000)")
plot.temporal.map("ideo_mean_2020", "darkblue", "red", "Average DW Nom Scores (2020)")
plot.temporal.map("ideo.shift.00.20", "darkblue", "red", "Shift in Average DW Nom Scores by State", "2000 to 2020")


# ------ Plotting Trends
# Correlation b/w increase in Hispanic % and Ideological shift by state
wsl %>% 
        select(state, h.shift.00.20, ideo.shift.00.20) %>% 
        ggplot(aes(x = h.shift.00.20, y = ideo.shift.00.20)) +
        geom_point(size = 5, alpha = 0.65) +
        geom_text(aes(label = state, vjust = -1.5)) +
        theme_minimal() +
        labs(x = "Increase in Hispanic Population %",
             y = "Ideological Shift (+Conservative")

# Correlation b/w decrease in NHW % and Ideological shift by state
wsl %>% 
        select(state, nhw.shift.00.20, ideo.shift.00.20) %>% 
        ggplot(aes(x = nhw.shift.00.20, y = ideo.shift.00.20)) +
        geom_point(size = 5, alpha = 0.65) +
        geom_text(aes(label = state, vjust = -1.5)) +
        theme_minimal() +
        labs(x = "Decrease in Non-Hispanic White Population %",
             y = "Ideological Shift (+Conservative")
