from typing import Union

from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC


class GenderEstimator(BaseEstimator):
    def __init__(self, max_features:int = 1000, C: float = 1.0, gamma: Union[str, float] = 'scale'):
        self.max_features = max_features
        self.gamma = gamma
        self.C = C
        self.clf = None

    def fit(self, X, y):
        self.vectorizer = TfidfVectorizer(max_features=self.max_features)
        self.clf = SVC(C=self.C, gamma=self.gamma)

        X_vectorized = self.vectorizer.fit_transform(X)
        self.clf.fit(X_vectorized, y)

    def predict(self, X):
        X_vectorized = self.vectorizer.transform(X)
        return self.clf.predict(X_vectorized)

    def score(self, X, y):
        X_vectorized = self.vectorizer.transform(X)
        return self.clf.score(X_vectorized, y)
