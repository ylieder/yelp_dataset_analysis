import pickle
from math import ceil

from sklearn.model_selection import GridSearchCV, PredefinedSplit, train_test_split
import numpy as np

from GenderEstimator import GenderEstimator


def main():
    """
    Runs an extensive grid search for n_reviews = 1, 2, 5, 10, 'all', Hyperparameters C = 0.1, 1, 10, 100, 1000
    and max_features = 500, 1000, 5000, 10000.

    Outputs the best parameters for each n in n_reviews.
    """
    for n_reviews in (1, 2, 5, 10, 'all'):
        print("n_reviews: ", n_reviews)

        n_samples = 20_000

        dataset_path = f'data/datasets/dataset_{n_reviews}_train.pkl'
        with open(dataset_path, 'rb') as fd:
            data = pickle.load(fd)
            X_train = [' '.join(reviews) for gender, reviews in data][:n_samples]
            y_train = [gender for gender, reviews in data][:n_samples]

        validation_size = 0.25
        test_size = 0.25
        train_size = 1 - test_size - validation_size

        corpus_train, corpus_test, y_train, y_test = train_test_split(X_train, y_train, test_size=test_size)

        param_grid = {
            'max_features': [500, 1000, 5000, 10000],
            'C': [0.01, 0.1, 1, 10, 100, 1000],
        }

        ps = PredefinedSplit(test_fold=np.concatenate(
            (-np.ones(int(train_size * len(X_train))), np.zeros(ceil(validation_size * len(X_train)))))
        )
        gs = GridSearchCV(GenderEstimator(), param_grid, cv=ps, n_jobs=4, verbose=3)

        gs.fit(corpus_train, y_train)

        best_score = gs.best_score_
        best_params = gs.best_params_

        print("Best parameters: ", best_params)
        print("Best score: ", best_score)


if __name__ == "__main__":
    main()