import os
import argparse

from GenderGuesser import GenderGuesser
from YelpDataset import YelpDataset


def main():
    parser = argparse.ArgumentParser(description='Create SQLite database from Yelp dataset JSONs.')
    parser.add_argument('database_path', type=str,
                        help='Path to sqlite database')
    parser.add_argument('--gender', '-g', action='store_true',
                        help='Add gender information to users')
    parser.add_argument('--language', '-l', action='store_true',
                        help='Add language information to reviews')
    parser.add_argument('--json_dir', type=str, help='Path to Yelp dataset JSON files')

    args = parser.parse_args()

    yelp = YelpDataset(args.database_path)

    if not os.path.exists(args.database_path):
        if not args.json_dir:
            print("Specify Yelp dataset JSON directory")
            return
        yelp.load_data(args.json_dir)
    else:
        print("Database alreay exists. Skip data filling")

    yelp.connect()

    batch_size = 100_000
    if args.gender:
        print('Add Gender information', end=' ')

        gg = GenderGuesser(os.path.join(os.path.dirname(__file__), 'data/names/yob2019.txt'))

        n_users = yelp.users.count()

        for i in range(0, n_users, batch_size):
            stop = min(i + batch_size, n_users)
            for user in yelp.users.slice(i, stop):
                user.gender = gg.guess(user.name)

            yelp.session.commit()
            print('#', end='')
        print()

    if args.language:
        try:
            import cld3

            print('Add language information', end=' ')
            n_reviews = yelp.reviews.count()

            for i in range(0, n_reviews, batch_size):
                stop = min(i + batch_size, n_reviews)
                for review in yelp.reviews.slice(i, stop):
                    lang_pred = cld3.get_language(review.text)
                    if lang_pred.is_reliable:
                        review.language = lang_pred.language
                yelp.session.commit()
                print('#', end='')
        except ModuleNotFoundError:
            print("Install pycld3 in order to add language information")

    yelp.close_session()


if __name__ == '__main__':
    main()

