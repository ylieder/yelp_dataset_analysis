import pickle
from datetime import timedelta
from pathlib import Path
import sys
from timeit import default_timer as timer

from sklearn.metrics import classification_report

from GenderEstimator import GenderEstimator


def main():
    data_dir = Path('data/datasets')
    estimator_dir = Path('data/estimators')
    estimator_dir.mkdir(exist_ok=True)

    if len(sys.argv) != 2:
        print("Specify number of reviews per sample (1, 2, 5, 10, 20 or all)")

    n_reviews = sys.argv[1]
    print("n_reviews: ", n_reviews)

    with open(data_dir / f'dataset_{n_reviews}_train.pkl', 'rb') as fd:
        data = pickle.load(fd)
        X_train = [''.join(reviews) for gender, reviews in data]
        y_train = [gender for gender, reviews in data]

    with open(data_dir / f'dataset_{n_reviews}_test.pkl', 'rb') as fd:
        data = pickle.load(fd)
        X_test = [''.join(reviews) for gender, reviews in data]
        y_test = [gender for gender, reviews in data]

    estimator = GenderEstimator(max_features=10_000, C=1.0)

    start = timer()
    estimator.fit(X_train, y_train)
    end = timer()
    print(f"Fit estimator in {timedelta(seconds=end-start)}")

    with open(estimator_dir / f'estimator_{n_reviews}.pkl', 'wb') as fd:
        pickle.dump(estimator, fd)

    # training_score = estimator.score(X_train, y_train)
    # print(f"Training accuracy: {training_score}")

    y_pred = estimator.predict(X_test)
    print(classification_report(y_test, y_pred))


if __name__ == '__main__':
    main()