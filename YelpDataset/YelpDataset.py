from pathlib import Path
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import Query, sessionmaker

from YelpDataset import create_sqlite_db

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
