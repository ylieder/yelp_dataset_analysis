from __future__ import annotations
import json
from datetime import datetime, timedelta
from pathlib import Path
from timeit import default_timer as timer
from typing import Any, Dict, List, Union, TYPE_CHECKING

from sqlalchemy import create_engine, Table
from sqlalchemy.exc import OperationalError

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

from .MappingDict import MappingDict
from .models import Base, YelpBusiness, YelpCategory, YelpCategoryBusinessRel, YelpCity, YelpUser, YelpReview

BATCH_SIZE = 100_000
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def create_sqlite_db(connection_string: str, data_dir: Union[str, Path]) -> None:
    """
    Creates an sqlite database according to the connection string and fills it with the Yelp dataaset located in
    data_dir.

    :param connection_string: Sqlite connection string to new database.
    :param data_dir: Yelp dataset directory.
    """
    print("Create tables")
    engine = create_engine(connection_string, echo=False)
    try:
        Base.metadata.create_all(engine, checkfirst=False)
    except OperationalError:
        raise RuntimeError("Database already exists")

    data_dir = Path(data_dir)

    business_mapping = _insert_businesses(engine, data_dir / 'yelp_academic_dataset_business.json')
    user_mapping = _insert_users(engine, data_dir / 'yelp_academic_dataset_user.json')
    _insert_reviews(
        engine,
        data_dir / 'yelp_academic_dataset_review.json',
        business_mapping,
        user_mapping,
    )


def _insert_data(engine: Engine, table: Union[Table, Base], buffer: List[Dict[str, Any]]) -> None:
    """
    Inserts all records stored in buffer to the specified table using the specified engine. Does nothing, if buffer is
    empty.

    :param engine: Database engine.
    :param table: Database table, records are inserted into.
    :param buffer: List of new data to be inserted.
    """
    if len(buffer) > 0:
        if isinstance(table, Table):
            engine.execute(table.insert(), buffer)
        else:
            engine.execute(table.__table__.insert(), buffer)


def _insert_businesses(engine: Engine, json_path: Union[str, Path]) -> Dict[str, int]:
    """
    Fills business table with data from 'yelp_academic_dataset_business.json'.

    :param engine: Database engine.
    :param json_path: Path to 'yelp_academic_dataset_business.json'.
    :return: Mapping from Yelp business_ids to database primary keys.
    """
    print("Insert businesses", end=' ')

    start_time = timer()

    category_mapping = MappingDict()
    city_mapping = MappingDict()
    business_mapping = {}
    buffer_city, buffer_category, buffer_business, buffer_cat_bus_rel = [], [], [], []
    with open(json_path, 'r') as fd:
        for idx, line in enumerate(fd):
            data = json.loads(line)

            city_id, created = city_mapping[(data['city'], data['state'])]
            if created:
                buffer_city.append({'id': city_id, 'name': data['city'], 'state': data['state']})

            categories = data['categories']
            if categories is not None:
                for category in categories.split(','):
                    category_id, created = category_mapping[category.strip()]
                    if created:
                        buffer_category.append({'id': category_id, 'name': category.strip()})
                    buffer_cat_bus_rel.append({'business_id': idx, 'category_id': category_id})

            buffer_business.append({
                'id': idx,
                'business_id': data['business_id'],
                'name': data['name'],
                'address': data['address'],
                'postal_code': data['postal_code'],
                'latitude': data['latitude'],
                'longitude': data['longitude'],
                'stars': data['stars'],
                'review_count': data['review_count'],
                'city_id': city_id,
            })
            business_mapping[data['business_id']] = idx

            if (idx + 1) % BATCH_SIZE == 0:
                print('#', end='')
                _insert_data(engine, YelpCategory, buffer_category)
                _insert_data(engine, YelpCity, buffer_city)
                _insert_data(engine, YelpBusiness, buffer_business)
                _insert_data(engine, YelpCategoryBusinessRel, buffer_cat_bus_rel)
                buffer_city, buffer_category, buffer_business, buffer_cat_bus_rel = [], [], [], []

    _insert_data(engine, YelpCategory, buffer_category)
    _insert_data(engine, YelpCity, buffer_city)
    _insert_data(engine, YelpBusiness, buffer_business)
    _insert_data(engine, YelpCategoryBusinessRel, buffer_cat_bus_rel)

    seconds_per_records = BATCH_SIZE * (timer() - start_time) / idx
    print(f"# ({timedelta(seconds=seconds_per_records)} per {BATCH_SIZE} records)")
    return business_mapping


def _insert_users(engine: Engine, json_path: Union[str, Path]) -> Dict[str, int]:
    """
    Fills user table with data from 'yelp_academic_dataset_user.json'.

    :param engine: Database engine.
    :param json_path: Path to 'yelp_academic_dataset_user.json'.
    :return: Mapping from Yelp user_ids to database primary keys.
    """
    print("Insert users", end=' ')

    start_time = timer()

    user_mapping = {}
    buffer_user = []
    with open(json_path, 'r') as fd:
        for idx, line in enumerate(fd):
            data = json.loads(line)
            del data['friends']
            data['yelping_since'] = datetime.strptime(data['yelping_since'], DATE_FORMAT)
            buffer_user.append({'id': idx, **data})
            user_mapping[data['user_id']] = idx

            if (idx + 1) % BATCH_SIZE == 0:
                print('#', end='')
                _insert_data(engine, YelpUser, buffer_user)
                buffer_user = []
        _insert_data(engine, YelpUser, buffer_user)

    seconds_per_records = BATCH_SIZE * (timer() - start_time) / idx
    print(f"# ({timedelta(seconds=seconds_per_records)} per {BATCH_SIZE} records)")
    return user_mapping


def _insert_reviews(
        engine: Engine, json_path: Union[str, Path], business_mapping: Dict[str, int], user_mapping: Dict[str, int]
) -> None:
    """
    Fills business table with data from 'yelp_academic_dataset_review.json'.

    :param engine: Database engine.
    :param json_path: Path to 'yelp_academic_dataset_review.json'.
    """
    print("Insert reviews", end=' ')

    start_time = timer()

    with open(json_path, 'r') as fd:
        buffer_review = []
        for idx, line in enumerate(fd):
            data = json.loads(line)
            data['business_id'] = business_mapping[data['business_id']]
            data['user_id'] = user_mapping[data['user_id']]
            data['date'] = datetime.strptime(data['date'], DATE_FORMAT)

            buffer_review.append({
                'id': idx, **data,
            })

            if (idx + 1) % BATCH_SIZE == 0:
                print('#', end='')
                _insert_data(engine, YelpReview, buffer_review)
                buffer_review = []
        _insert_data(engine, YelpReview, buffer_review)

    seconds_per_records = BATCH_SIZE * (timer() - start_time) / idx
    print(f"# ({timedelta(seconds=seconds_per_records)} per {BATCH_SIZE} records)")
