from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score

import pandas as pd
import numpy as np

logreg_param_grid = {
  'solver': ['liblinear', 'lbfgs'],
  'C': np.logspace(-2, 4, 10),
  # 'penalty': ['l1', 'l2']
}

mlpc_param_grid = {
  'solver': ['lbfgs', 'adam'],
  'alpha': np.logspace(-4, 2, 4),
  'activation': ['logistic', 'relu']
}

dtree_param_grid = {
  'criterion': ['gini', 'entropy'],
  'splitter': ['best', 'random'],
  'min_samples_split' : range(10,200,20),
  'max_depth': range(1,15,2)
}

classifiers = [
  ('LogisticRegression', LogisticRegression(max_iter=300), logreg_param_grid),
  # ('MLPClassifier', MLPClassifier(max_iter=1000), mlpc_param_grid),
  ('DecisionTreeClassifier', tree.DecisionTreeClassifier(), dtree_param_grid)
]

def train(df):
  best_estimators = []
  feature_cols = df.columns.difference(['StatusFinal', 'StudentId'])
  features = df.loc[:, feature_cols] # we want all rows and the features columns
  labels = df.StatusFinal.replace({'EVADIDO': 1, 'FORMADO': 0})  # our label is StatusFinal

  for classifier in classifiers:
    print(classifier[0])
    grid_search = GridSearchCV(classifier[1], classifier[2], scoring='recall',
                              cv=10, return_train_score=True)
    grid_search.fit(features, labels)

    print('Best params for recall', grid_search.best_params_)
    print('Best estimator', grid_search.best_estimator_)
    print("Best recall = ", grid_search.best_score_)

    best_estimators.append(grid_search.best_estimator_)
  
  return best_estimators

