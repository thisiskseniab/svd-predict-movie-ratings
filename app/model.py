from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable=True)
	password = Column(String(64), nullable=True)
	age = Column(Integer, nullable=True)
	zipcode = Column(String(15), nullable=True)

	def __init__(self, email = None, password = None, age = None, zipcode = None):
		self.email = email
		self.password = password
		self.age = age
		self.zipcode = zipcode

class Movie(Base):
	__tablename__ = "movies"

	id = Column(Integer, primary_key = True)
	title = Column(String(64))
	genre = Column(String(256))

	def __init__(self, title, genre):
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
	global ENGINE
	global Session

	ENGINE = create_engine("sqlite:///data/ratings.db") #, echo=True)
	Session = sessionmaker(bind=ENGINE)

	return Session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
