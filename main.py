import sys

from YelpDataset import YelpDataset


if __name__ == '__main__':
    database_file = sys.argv[1]
    yelp_json_dir = sys.argv[2]

    yelp = YelpDataset(database_file)
    yelp.load_data(yelp_json_dir)

    if len(sys.argv) == 4:
        namelist_file = sys.argv[3]
        yelp.add_gender_data(namelist_file)
