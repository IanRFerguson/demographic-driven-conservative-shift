# This script sets up our environment for all analyses we'll want to use
# at this stage ... we'll source it out

# ---- Imports + Setup
library(tidyverse)
library(tidytext)
library(lubridate)
library(ggridges)

here <- "~/Box Sync/Research/Ian/DEMOGRAPHICS/conservatism-demographics/"
setwd(here)

tweets <- read_csv('./data/tweet-data/all-tweets-scraped.csv') %>% 
        # Drop index column 
        select(!X1) %>% 
        
        # Convert racial change bin to ordered factor
        mutate(`hispanic-pop-change` = factor(`hispanic-pop-change`, levels = c('low', 'mid', 'high'))) %>% 
        
        # Drop duplicate speakers
        group_by(UserName) %>% slice(1) %>% ungroup() %>% 
        
        # Oldest tweets first
        arrange(DateTime)

# Define custom color palette
my_colors <- c("#00798c", "#d1495b", "#edae49", "#66a182", "#2e4057", "#8d96a3", "#000000")


# Summary table of averages and totals per racial change bin
summary.table <- tweets %>% 
                        group_by(`hispanic-pop-change`) %>% 
                        summarise(total.tweets = n(),
                                  total.hate.tweets = sum(`predicted-hs` == 1),
                                  hate.tweet.pct = total.hate.tweets / total.tweets,
                                  total.mentions = sum(is_mention == 1),
                                  mention.pct = total.mentions / total.tweets,
                                  hate.speech.mentions = sum(`predicted-hs` == 1 & is_mention == 1),
                                  hate.mention.pct = hate.speech.mentions / total.mentions) %>% 
                        ungroup()
