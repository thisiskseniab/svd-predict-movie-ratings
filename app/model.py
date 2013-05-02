from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()
global ENGINE
global session
ENGINE = create_engine("sqlite:///ratings.db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))
Base.query = session.query_property()




### Class declarations go here

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	indx = Column(Integer)
	email = Column(String(64), nullable=True)
	password = Column(String(64), nullable=True)
	name = Column(String(64), nullable=True)

	def __init__(self, indx, email = None, password = None, name = None):
		self.indx = indx
		self.email = email
		self.password = password
		self.name = name


class Movie(Base):
	__tablename__ = "movies"

	id = Column(Integer, primary_key = True)
	indx = Column(Integer)
	title = Column(String(128))
	genre = Column(String(128))

	def __init__(self, indx, title, genre):
		self.indx = indx
		self.title = title
		self.genre = genre


class Rating(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	user_indx = Column(Integer)
	movie_indx = Column(Integer)
	rating = Column(Integer)
	timestamp = Column(Integer)

	def __init__(self, user_indx, movie_indx, rating, timestamp):
		self.user_indx = user_indx
		self.movie_indx = movie_indx
		self.rating = rating
		self.timestamp = timestamp


class Tag(Base):
	__tablename__ = "tags"

	id = Column(Integer, primary_key = True)
	user_indx = Column(Integer)
	movie_indx = Column(Integer)
	tag = Column(String(256))
	timestamp = Column(Integer)

	def __init__(self, user_indx, movie_indx, tag, timestamp):
		self.user_indx = user_indx
		self.movie_indx = movie_indx
		self.tag = tag
		self.timestamp = timestamp


### End class declarations

def connect():
	#use this for seeding the db
	engine = create_engine("sqlite:///ratings.db", echo=False)
	session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))


	Base = declarative_base()
	Base.query = session.query_property()
	

	return session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
