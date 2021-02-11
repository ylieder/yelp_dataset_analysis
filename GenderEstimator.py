from typing import Union

from sklearn.base import BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC


class GenderEstimator(BaseEstimator):
    """
    Estimator to predict gender of a Yelp user given her written reviews.
    """
    def __init__(self, max_features: int = 1000, C: float = 1.0, gamma: Union[str, float] = 'scale'):
        """
        :param max_features: Maximum number of features, extracted from the train dataset.
        :param C: Regularization parameter of the SVM.
        :param gamma: Kernel coefficient for RBF kernel of the SVM.
        """
        self.max_features = max_features
        self.gamma = gamma
        self.C = C
        self.clf = None
        self.vectorizer = None

    def fit(self, X, y):
        """
        :param X: Training data (reviews). One review per sample. Multiple reviews should be merged before.
        :param y: Training labels (gender). Either Gender.F or Gender.M.
        """
        self.vectorizer = TfidfVectorizer(max_features=self.max_features)
        self.clf = SVC(C=self.C, gamma=self.gamma)

        X_vectorized = self.vectorizer.fit_transform(X)
        self.clf.fit(X_vectorized, y)

    def predict(self, X):
        """
        :param X: List of reviews, one review per sample. Multiple reviews should be merged before.
        :return: Predicted gender of each sample.
        """
        X_vectorized = self.vectorizer.transform(X)
        return self.clf.predict(X_vectorized)

    def score(self, X, y):
        """
        Same as predict, but computes accuracy between prediction and y.

        :param X: List of reviews, one review per sample. Multiple reviews should be merged before.
        :param y: True gender.
        """
        X_vectorized = self.vectorizer.transform(X)
        return self.clf.score(X_vectorized, y)
