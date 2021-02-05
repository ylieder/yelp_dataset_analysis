from sqlalchemy import Column, Date, Float, ForeignKey, Integer, SmallInteger, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


"""
Relation table between Yelp categories and Yelp businesses.
"""
YelpCategoryBusinessRel = Table(
    'business_category_rel', Base.metadata,
    Column('business_id', String, ForeignKey('business.id')),
    Column('category_id', Integer, ForeignKey('category.id')),
)


class YelpCategory(Base):
    """
    Yelp Category table.
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class YelpCity(Base):
    """
    Yelp City table.
    """
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    state = Column(String)


class YelpBusiness(Base):
    """
    Yelp Business table.
    """
    __tablename__ = 'business'

    id = Column(Integer, primary_key=True)
    business_id = Column(String, primary_key=True)
    name = Column(String)
    address = Column(String)
    postal_code = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    stars = Column(Float)
    review_count = Column(Integer)

    city_id = Column(Integer, ForeignKey(YelpCity.id))

    city = relationship(YelpCity, backref='businesses')
    categories = relationship(YelpCategory, secondary=YelpCategoryBusinessRel, backref='businesses')


class YelpUser(Base):
    """
    Yelp User table.
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    name = Column(String)
    review_count = Column(Integer)
    yelping_since = Column(Date)
    useful = Column(Integer)
    funny = Column(Integer)
    cool = Column(Integer)
    elite = Column(String)
    fans = Column(Integer)
    average_stars = Column(Float)
    compliment_hot = Column(Integer)
    compliment_more = Column(Integer)
    compliment_profile = Column(Integer)
    compliment_cute = Column(Integer)
    compliment_list = Column(Integer)
    compliment_note = Column(Integer)
    compliment_plain = Column(Integer)
    compliment_cool = Column(Integer)
    compliment_funny = Column(Integer)
    compliment_writer = Column(Integer)
    compliment_photos = Column(Integer)
    gender = Column(SmallInteger)


class YelpReview(Base):
    """
    Yelp Review Table.
    """
    __tablename__ = 'review'

    id = Column(Integer, primary_key=True)
    review_id = Column(String)
    stars = Column(Float)
    useful = Column(Integer)
    funny = Column(Integer)
    cool = Column(Integer)
    text = Column(String)
    date = Column(Date)

    user_id = Column(Integer, ForeignKey(YelpUser.id))
    business_id = Column(Integer, ForeignKey(YelpBusiness.id))

    user = relationship(YelpUser, backref='reviews')
    business = relationship(YelpBusiness, backref='reviews')
