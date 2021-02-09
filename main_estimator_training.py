import pickle
from datetime import timedelta
from pathlib import Path
import sys
from timeit import default_timer as timer

from sklearn.metrics import classification_report

from GenderEstimator import GenderEstimator


def train_gender_estimator(n_reviews, max_features):
    """
    Trains a gender estimator with C=1.
    
    :param n_reviews: Specifies the dataset to be used for training (number of reviews per user).
    :param max_features: Maximum number of features.
    """
    data_dir = Path('data')
    dataset_path = data_dir / f'datasets/dataset_{n_reviews}_train.pkl'
    estimator_dir = data_dir / 'estimators'
    estimator_dir.mkdir(exist_ok=True)

    with open(dataset_path, 'rb') as fd:
        data = pickle.load(fd)
        X_train = [' '.join(reviews) for gender, reviews in data]
        y_train = [gender for gender, reviews in data]

    estimator = GenderEstimator(max_features=max_features, C=1.0)

    start = timer()
    estimator.fit(X_train, y_train)
    end = timer()
    print(f"Fit estimator in {timedelta(seconds=end-start)}")

    output_path = estimator_dir / f'estimator_{n_reviews}.pkl'
    with open(output_path, 'wb') as fd:
        pickle.dump(estimator, fd)
        print(f"Export trained estimate to {output_path}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Specify number of reviews per user")
        
    if len(sys.argv) == 3:
        max_features = int(sys.argv[2])
    else:
        max_features = 10_000
    
    dataset_path = sys.argv[1]
    train_gender_estimator(dataset_path, max_features)