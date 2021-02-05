from pathlib import Path
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import Query, sessionmaker

from YelpDataset import create_sqlite_db
from .GenderGuesser import GenderGuesser

from .models import *


class YelpDataset:
    def __init__(self, path: Union[str, Path]):
        """
        :param path: Path to Yelp sqlite database
        """
        self._connection_string = f'sqlite:///{path}'
        self.session = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()

    def connect(self) -> None:
        """
        Establishs connection to the Yelp sqlite database.
        """
        engine = create_engine(self._connection_string, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_session(self) -> None:
        """
        Closes the session if connection to Yelp sqlite database is open.
        """
        if self.session:
            self.session.close()
            self.session = None

    @property
    def businesses(self) -> Query:
        """
        :return: Query over business table.
        """
        return self.session.query(YelpBusiness)

    @property
    def users(self) -> Query:
        """
        :return: Query over user table.
        """
        return self.session.query(YelpUser)

    @property
    def reviews(self) -> Query:
        """
        :return: Query over review table.
        """
        return self.session.query(YelpReview)

    def load_data(self, data_dir: Union[str, Path]) -> None:
        """
        Creates database initially and fills it with the Yelp dataset.

        :param data_dir: Path to Yelp dataset directory (contains a json for each table).
        """
        create_sqlite_db(self._connection_string, data_dir)

    def add_gender_data(self, names_file_path: Union[str, Path], batch_size: int = 100000) -> None:
        """
        Iterates over all users and add missing gender information by looking up names in a name database.

        :param names_file_path: Path to CSV file with (name, gender) records.
        :param batch_size: Batch size of processed user records until database commit.
        """
        print('Add Gender information', end=' ')

        disconnected = False
        if self.session is None:
            disconnected = True
            self.connect()

        gg = GenderGuesser(names_file_path)

        n = self.users.count()

        for i in range(0, n, batch_size):
            for user in self.users[i:i+batch_size]:
                user.gender = gg.guess(user.name).value
            self.session.commit()
            print('#', end='')

        if disconnected:
            self.close_session()

        print()
