"""
Date: 4/20/2019
Authors: Raymond Pistoresi
Version: 1.00
"""
import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

class CatToyModel:

  def __init__(self, data_file):
    self.dataset_file = data_file
    self.answers_file = 'answers.csv'
    self.dataset = []
    self.stemmed_dataset = []
    self.X = []
    self.y = []
    self.X_train = []
    self.X_test = []
    self.y_train = []
    self.y_test = []

  def categorize_dataset(self):
    self.dataset = pd.read_csv(self.dataset_file, delimiter = ',')

    for index, row in self.dataset.iterrows():
      if row['Rating'] > 3:
        self.dataset.loc[index, 'Rating'] = 1
      else:
        self.dataset.loc[index, 'Rating'] = 0

    self.dataset.to_csv(self.answers_file)
    self.dataset = pd.read_csv(self.answers_file, delimiter = ',')

  def clean_dataset(self):
    for i in range(len(self.dataset)):
      review = re.sub('[^a-zA-Z]', ' ', self.dataset['Review'][i])
      review = review.lower().split()

      # take main stem of each word
      ps = PorterStemmer()
      review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
      review = ' '.join(review)
      self.stemmed_dataset.append(review)

  def select_features(self):
    cv = CountVectorizer(max_features=500)

    # X : dependant variable, y : answers if review is positive or negative
    self.X = cv.fit_transform(self.stemmed_dataset).toarray()
    self.y = self.dataset.iloc[:, 2].values

  def split_dataset(self):
    self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.25)

  def create_model(self):
    model = RandomForestClassifier(n_estimators=501, criterion='entropy')
    model.fit(self.X_train, self.y_train)
    self.y_pred = model.predict(self.X_test)

  def get_accuracy_score(self):
    return accuracy_score(self.y_test, self.y_pred)

  def predict(self):
    cpt.categorize_dataset()
    cpt.clean_dataset()
    cpt.select_features()
    cpt.split_dataset()
    cpt.create_model()
    return cpt.get_accuracy_score()

if __name__ == '__main__':
  asin = ['B009R3SFBC', 'B072WCZQ4V', 'B06WP7F8YC', 'B00TTU9RAQ', 'B000IYSAIW']
  print('starting...')
  for i in range(len(asin)):
    cpt = CatToyModel('./datasets/reviews_{}.csv'.format(asin[i]))
    score = '{}: {}'.format(asin[i], cpt.predict())
    print(score)
  print('finished.')
