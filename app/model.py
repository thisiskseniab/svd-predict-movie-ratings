from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()
global ENGINE
global session

ENGINE = create_engine("sqlite:///ratings.db", echo=True)
# session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))
# Base.query = session.query_property()




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
	user_id = Column(Integer)
	movie_id = Column(Integer)
	rating = Column(Integer)
	timestamp = Column(Integer)

	def __init__(self, user_id, movie_id, rating, timestamp):
		self.user_id = user_id
		self.movie_id = movie_id
		self.rating = rating
		self.timestamp = timestamp


class Tag(Base):
	__tablename__ = "tags"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer)
	movie_id = Column(Integer)
	tag = Column(String(256))
	timestamp = Column(Integer)

	def __init__(self, user_id, movie_id, tag, timestamp):
		self.user_id = user_id
		self.movie_id = movie_id
		self.tag = tag
		self.timestamp = timestamp


### End class declarations

def connect():
	engine = create_engine("sqlite:///ratings.db", echo=False)
	session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))


	Base = declarative_base()
	Base.query = session.query_property()
	# global ENGINE
	# global Session

	# ENGINE = create_engine("sqlite:///ratings.db", echo=True)
	# Session = scoped_session(sessionmaker(bind=Engine, autocommit = False, autoflush = False))
	# Base.query = Session.query_property()

	return session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
