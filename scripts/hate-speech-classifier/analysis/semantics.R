# Goals of this Script
# Tokenize words from tweets
# Assess AFINN polarity
# Determine if negative affect more likely in high change bin
#
# Ian Richard Ferguson | Stanford University

setwd("~/Box Sync/Research/Ian/DEMOGRAPHICS/conservatism-demographics/scripts/hate-speech-classifier/analysis/")
source("setup.R")

tweets <- tweets %>% 
        mutate(
                # Add index column to keep track of tweet corpus
                idx = row_number()
        )

# DataFrame of tokenized words and their respective polarity values
tokenized.data <- tweets %>% 
        # Remove rows with no text data
        filter(!is.na(Tweet)) %>% 
        
        # Tokenize tweet corpus
        unnest_tokens(word, Tweet, token = "tweets") %>% 
        
        # Remove any stray characters
        filter(!str_detect(word, "^[0-9]*$")) %>% 
        
        # Filter out all stop words
        anti_join(stop_words) %>% 
        
        # Isolate word stem wherever possible
        mutate(word = SnowballC::wordStem(word)) %>% 
        
        # Join DataFrame with AFINN polarity scores
        left_join(get_sentiments("afinn")) %>% 
        
        # Drop rows with Null polarity value
        filter(!is.na(value))


# Summary table of average AFINN scores / tweet
summary.tokens <- tokenized.data %>% 
        # Group by row index
        group_by(idx) %>% 
        summarise(
                # Average AFINN polarity score
                mean.score = mean(value, na.rm = T),
                
                # Racial change bin from tweet author
                bin = first(`hispanic-pop-change`),
                  
                # Binary hate speech value
                is.hate.speech = first(`predicted-hs`),
                  
                # Binary tweet type value
                is.mention = first(is_mention)
        )

# Plot ridge plots for all tweets by racial change bin
summary.tokens %>% 
        ggplot(aes(x = mean.score, y = bin, fill = bin)) +
        geom_density_ridges(alpha = 0.95, color = "black", panel_scaling = F) +
        scale_fill_manual(values=c(my_colors[3], my_colors[2], my_colors[1])) +
        theme_minimal() +
        labs(x = "AFINN Polarity Values", y ="",
             title = "All Tweets", subtitle = "Polarity Distribtuion by Racial Change Bin") +
        theme(legend.position = "none",
              plot.title = element_text(hjust = 0.5, face = 'bold'),
              plot.subtitle = element_text(hjust = 0.5)) +
        scale_y_discrete(labels=c('High', 'Mid', 'Low'))


# Plot ridge plots for hate speech tweets by racial change bin
summary.tokens %>% 
        filter(is.hate.speech == 1) %>% 
        ggplot(aes(x = mean.score, y = bin, fill = bin)) +
        geom_density_ridges(alpha = 0.95, color = "black") +
        scale_fill_manual(values=c(my_colors[3], my_colors[2], my_colors[1])) +
        theme_minimal() +
        labs(x = "AFINN Polarity Values", y ="", ccaption = "Mentions Only") +
        theme(legend.position = "none") +
        scale_y_discrete(labels=c('High', 'Mid', 'Low'))


tokenized.data %>% 
        filter(idx <= 125) %>% 
        select(word, value) %>% 
        group_by(word) %>% 
        summarise(count = n(), value = first(value)) %>% 
        mutate(fill_color = ifelse(value > 0, T, F)) %>% 
        arrange(desc(value)) %>% 
        ggplot(aes(x = value, y = reorder(word, +value), fill = fill_color)) +
        geom_col(alpha = 0.95) +
        scale_fill_brewer(palette = "Set1") +
        theme_minimal() +
        labs(x = "AFINN Polarity Value", y = "") +
        theme(legend.position = "none")

tokenized.data %>% 
        ggplot(aes(x = value)) +
        geom_density(fill = my_colors[4]) +
        theme_minimal() +
        labs(x = "AFINN Polarity Value", y = "") +
        coord_cartesian(xlim = c(-6, 6))
