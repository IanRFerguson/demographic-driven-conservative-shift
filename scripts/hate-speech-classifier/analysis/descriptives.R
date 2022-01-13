# Goals of this Script
# Breakdown descriptive stats of tweets (% of hate speech, for example)
#
# Ian Richard Ferguson | Stanford University

setwd('~/Box Sync/Research/Ian/DEMOGRAPHICS/conservatism-demographics/scripts/hate-speech-classifier/analysis/')
source("setup.R")


# ---- Breakdown by bin
summary.table %>% 
        select(`hispanic-pop-change`, total.tweets, total.hate.tweets) %>% 
        pivot_longer(!`hispanic-pop-change`) %>% 
        rename(bin = `hispanic-pop-change`,
               subset = name) %>% 
        ggplot(aes(x = bin, y = value, fill = subset)) +
        geom_col(position = 'dodge') +
        theme_minimal() +
        labs(x = "", y = "count", 
             fill = "",
             title = "Tweets by Demographic Change Bin") +
        scale_fill_manual(values=my_colors[4:6], labels=c('Hate Tweets', 'Total Tweets')) +
        theme(plot.title = element_text(hjust = 0.5, face='bold'),
              legend.position = 'bottom')


summary.table %>% 
        select(`hispanic-pop-change`, total.mentions, hate.speech.mentions) %>% 
        pivot_longer(!`hispanic-pop-change`) %>% 
        rename(bin = `hispanic-pop-change`,
               subset = name) %>% 
        ggplot(aes(x = bin, y = value, fill = subset)) +
        geom_col(position='dodge') +
        theme_minimal() +
        labs(x = "", y = "count",
             fill = "",
             title = "Mentions by Demographic Change Bin") +
        scale_fill_manual(values=my_colors[4:6], labels=c('Hateful Mentions', 'Total Mentions')) +
        theme(plot.title = element_text(hjust = 0.5, face = 'bold'), 
              legend.position = 'bottom')
