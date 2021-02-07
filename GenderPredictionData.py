import json
import pickle
import re
from datetime import timedelta
import random
from typing import Optional
from timeit import default_timer as timer


from GenderGuesser import Gender, GenderGuesser


class GenderPredictionData:
    """
    Manages data for gender prediction tasks in sense of pickling, unpickling, reading from JSON, shuffling,
    transforming.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.data = None

    def read_data(self, yelp_dataset_dir, name_list_file):
        """
        Reads the Yelp user and review JSON files and extracts the reviews of all users whose names are either male or
        female.

        :param yelp_dataset_dir: Path to yelp dataset JSON files .
        :return: List of tuples (gender, reviews) for each user with a male or female name.
        """
        gender_guesser = GenderGuesser(name_list_file)
        data = dict()

        start = timer()
        with open(f'{yelp_dataset_dir}/yelp_academic_dataset_user.json', 'r') as fd:
            for line in fd:
                record = json.loads(line)

                gender = gender_guesser.guess(record['name'])
                if gender in (Gender.M, Gender.F):
                    data[record['user_id']] = (gender, [])

        with open(f'{yelp_dataset_dir}/yelp_academic_dataset_review.json', 'r') as fd:
            for line in fd:
                record = json.loads(line)

                if record['user_id'] in data:
                    data[record['user_id']][1].append(record['text'])

        end = timer()
        if self.verbose:
            print(f"Read JSON data in {timedelta(seconds=end-start)}")

        self.data = list(data.values())
        return self

    def min_review_num(self, n: int):
        if self.verbose:
            print(f"Drop all users with less than {n} reviews...")

        self.data = [x for x in self.data if len(x[1]) >= n]

        return self

    def shuffle(self):
        if self.verbose:
            print("Shuffle samples...")

        random.shuffle(self.data)

        return self

    def sanitize(self):
        if self.verbose:
            print("Sanitize review texts...")

        for _, review_list in self.data:
            for idx, review in enumerate(review_list):
                sanitized_review = re.sub(r'[\s,+&%$!?.*-]+', ' ', review)
                sanitized_review = re.sub(r'(\s|^)\d+(\.\d+)?(\s|$)', ' ', sanitized_review)
                sanitized_review = sanitized_review.lower()
                review_list[idx] = sanitized_review

        return self

    def shuffle_reviews(self):
        if self.verbose:
            print("Shuffle review lists...")

        for _, review_list in self.data:
            random.shuffle(review_list)

        return self

    def truncate(self, n: int):
        if self.verbose:
            print(f"Truncate review list to {n} review per sample...")

        for idx, (gender, review_list) in enumerate(self.data):
            self.data[idx] = (gender, review_list[:n])

        return self

    def merge(self):
        if self.verbose:
            print("Merge reviews...")

        for idx, (gender, review_list) in enumerate(self.data):
            self.data[idx] = (gender, [" ".join(review_list)])

        return self

    def balance(self, max_size_per_class: Optional[int] = None):
        if self.verbose:
            print(f"Balance dataset...")

        female_idxs = [i for i in range(len(self.data)) if self.data[i][0] == Gender.F][:max_size_per_class]
        male_idxs = [i for i in range(len(self.data)) if self.data[i][0] == Gender.M][:max_size_per_class]

        if len(female_idxs) > len(male_idxs):
            female_idxs = female_idxs[:len(male_idxs)]
        else:
            male_idxs = male_idxs[:len(female_idxs)]

        remaining_idxs = set(female_idxs) | set(male_idxs)
        self.data = [self.data[i] for i in range(self.size) if i in remaining_idxs]

        return self

    def shrink(self, size, balance: bool = False):
        if self.verbose:
            print(f"Shrink dataset to {size} samples...")

        if not balance:
            self.data = self.data[:size]
        else:
            self.balance(max_size_per_class=int(size / 2))

        return self

    @property
    def size(self):
        return len(self.data)

    def pickle(self, path):
        start = timer()
        with open(path, 'wb') as fd:
            pickle.dump(self.data, fd)
        end = timer()

        if self.verbose:
            print(f"Pickle data to {path} in {timedelta(seconds=end-start)}")

    def unpickle(self, path):
        with open(path, 'rb') as fd:
            self.data = pickle.load(fd)

        if self.verbose:
            print(f"Pickled data to {path}")
