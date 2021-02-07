import os
import pickle
from math import ceil

from sklearn.model_selection import GridSearchCV, PredefinedSplit, train_test_split
import numpy as np

from GenderEstimator import GenderEstimator
from GenderPredictionData import GenderPredictionData


def main():
    pkl_file_path = 'data/gender_prediction_data.pkl'
    yelp_dataset_dir = 'data/yelp_dataset'
    name_list_path = 'data/names/yob2019.txt'

    for n_reviews in (1, 2, 5, 10, 'all'):
        print("n_reviews: ", n_reviews)

        gpd = GenderPredictionData(verbose=True)

        if os.path.exists(pkl_file_path):
            gpd.unpickle(pkl_file_path)
        else:
            gpd.read_data(yelp_dataset_dir, name_list_path)
            gpd.pickle(pkl_file_path)

        if n_reviews != 'all':
            gpd.min_review_num(n_reviews).shuffle_reviews().truncate(n_reviews)
        else:
            gpd.shuffle_reviews()

        gpd.shuffle().shrink(40000, balance=True).shuffle_reviews().sanitize().merge()

        n_samples = gpd.size

        corpus = [reviews[0] for gender, reviews in gpd.data]
        labels = [gender for gender, reviews in gpd.data]

        validation_size = 0.25
        test_size = 0.25
        train_size = 1 - test_size - validation_size

        corpus_train, corpus_test, y_train, y_test = train_test_split(corpus, labels, test_size=test_size)

        param_grid = {
            'max_features': [500, 1000, 5000, 10000],
            'C': [0.01, 0.1, 1, 10, 100, 1000],
        }

        ps = PredefinedSplit(test_fold=np.concatenate(
            (-np.ones(int(train_size * n_samples)), np.zeros(ceil(validation_size * n_samples))))
        )
        gs = GridSearchCV(GenderEstimator(), param_grid, cv=ps, verbose=3)

        gs.fit(corpus_train, y_train)

        print(gs.score(corpus_test, y_test))

        best_estimator = gs.best_estimator_
        best_score = gs.best_score_
        best_params = gs.best_params_

        with open(f'best_estimator_{n_reviews}.pkl', 'wb') as fd:
            pickle.dump(best_estimator, fd)

        print(best_params)
        print(best_score)


if __name__ == "__main__":
    main()