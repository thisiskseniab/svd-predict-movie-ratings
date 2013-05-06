from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
global ENGINE
global session
ENGINE = create_engine("mysql+mysqldb://root@localhost/ratingsdb", echo=True)
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
	title = Column(String(256))
	genre = Column(String(128))

	def __init__(self, indx, title, genre):
		self.indx = indx
		self.title = title
		self.genre = genre

class Rating(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	user_indx = Column(Integer, ForeignKey('users.indx'))
	movie_indx = Column(Integer, ForeignKey('movies.indx'))
	rating = Column(Integer)
	timestamp = Column(Integer)

	def __init__(self, user_indx, movie_indx, rating, timestamp):
		self.user_indx = user_indx
		self.movie_indx = movie_indx
		self.rating = rating
		self.timestamp = timestamp
	
	user = relationship("User", backref=backref("rating", order_by=user_indx))
	movie = relationship("Movie", backref=backref("rating", order_by=movie_indx))

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


class Prediction(Base):
	__tablename__ = "predictions"

	id = Column(Integer, primary_key = True)
	user_indx = Column(Integer, ForeignKey('users.indx'))
	movie_indx = Column(Integer, ForeignKey('movies.indx'))
	rating_score = Column(Integer)
	
	def __init__(self, user_indx, movie_indx,rating_score):
		self.user_indx = user_indx
		self.movie_indx = movie_indx
		self.rating_score = rating_score

	user = relationship("User", backref=backref("prediction", order_by=user_indx))
	movie = relationship("Movie", backref=backref("prediction", order_by=movie_indx))

### End class declarations

def connect():
	#use this for seeding the db
	engine = create_engine("mysql+mysqldb://root@localhost/ratingsdb", echo=False)
	session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))


	Base = declarative_base()
	Base.query = session.query_property()
	

	return session()

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()

#to connect to mysql database ENGINE = create_engine("mysql+mysqldb://root@localhost", echo=True)
#to create mysql detabase ENGINE.execute("CREATE DATABASE ratingsdb")
#switch to it ENGINE.execute("USE ratingsdb")
# Base.metadata.create_all(ENGINE)
# OR: User.metadata.tables['movies'].create OR Base.metadata.tables['tablename'].create(ENGINE)
#to use mysql as user: mysql -u root
#then connect to db: use ratingsdb
#to view progress in mysql another window: select count(*) from users;
#delete everything from a table: truncate ratings;


