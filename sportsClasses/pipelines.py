import os

from sqlalchemy import String, Column, JSON, Integer, DateTime, Text, ForeignKey, Float
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

from sportsClasses.items import LocationItem, CourseItem, SportsClassItem

Base = declarative_base()
engine = create_engine(os.environ.get("DATABASE_URL"), echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class SportsClass(Base):
    __tablename__ = "class"
    id = Column(Integer, primary_key=True)
    last_run = Column(DateTime)
    name = Column(String(200), index=True)
    description = Column(Text)
    url = Column(String, unique=True)
    courses = relationship("Course", backref="class")


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    sports_class_url = Column(String, ForeignKey("class.url"))
    name = Column(String)
    day = Column(String)
    place = Column(String)
    price = Column(String)
    time = Column(String)
    timeframe = Column(String)
    bookable = Column(String)


class Location(Base):
    __tablename__ = "location"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lat = Column(Float)
    lon = Column(Float)


class DatabasePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, LocationItem):
            DBClass = Location
        elif isinstance(item, CourseItem):
            DBClass = Course
        elif isinstance(item, SportsClassItem):
            DBClass = SportsClass
        #TODO: Update existing
        try:
            db_item = DBClass(**item)
            session.add(db_item)
            session.commit()
        except:
            session.rollback()

