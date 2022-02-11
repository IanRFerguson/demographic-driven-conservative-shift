#!/bin/python3

"""
THANK YOU to Aman Kharwal for their excellent tutorial on
classifying hate speech! This script is based largely on
an article authored by AK, find it below:

https://thecleverprogrammer.com/2020/08/19/hate-speech-detection-model/
"""


# ---- Imports
import re, pickle
import pandas as pd
from sklearn.utils import resample
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split


# ---- Helpers
def clean_text_data(DF, VAR):
      """
      DF => Pandas DataFrame object
      VAR => Feature column to clean

      Removes extraneous letters from Tweet body

      Returns full DataFrame
      """

      # Transpose all text to lowercase 
      DF[VAR] = DF[VAR].str.lower()
      
      # Remove extraneous characters
      DF[VAR] = DF[VAR].apply(lambda x: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", x))

      

      # Remove all whitespace
      DF[VAR] = DF[VAR].str.strip()
                            
      return DF


def main():

      # Read in train data
      train_data = pd.read_csv('../../../data/tweet-data/hate-speech/train.csv')
      
      # Clean Tweet text
      train_data = clean_text_data(train_data, 'tweet')

      # ---- Balance dataset
      
      # Not labeled as Hate Speech
      t_maj = train_data[train_data['label'] == 0]
      
      # Labeled as Hate Speech
      t_min = train_data[train_data['label'] == 1]

      # Resample data to balance observation types
      t_unsampled = resample(t_min, replace=True, n_samples=len(t_maj), random_state=101)

      # Combine resampled data with majority data
      train_unsampled = pd.concat([t_unsampled, t_maj])

      # Instantiate three-level classification pipeline
      pipeline_sgd = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf',  TfidfTransformer()),
            ('nb', SGDClassifier()),])

      # Split data into training and testing components
      X_train, X_test, y_train, y_test = train_test_split(train_unsampled['tweet'], 
                                                          train_unsampled['label'],
                                                          random_state=101)

      # Fit pipeline to training data
      model = pipeline_sgd.fit(X_train, y_train)
      
      # Predict y values
      y_predict = model.predict(X_test)

      # Print accuracy score
      print(f'\nModel F1 score:\t\t{f1_score(y_predict, y_test)}')
      
      # Save classifier locally
      with open('../../../data/tweet-data/trained_hs_classifier.sav', 'wb') as outgoing:
            pickle.dump(model, outgoing)