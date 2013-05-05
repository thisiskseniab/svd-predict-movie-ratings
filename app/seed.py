import model
import csv
from datetime import datetime
import json

# All the paths for filenames in seed.py are relative to the project folder
# not the app/ directory, so i took '../' off the beginning

# get an id -> index json object for movies and users
with open('../data/ml-10M100K/user_id_to_index.json', 'r') as user_file:
    user_id_to_index = json.load(user_file)

with open('../data/ml-10M100K/movie_id_to_index.json', 'r') as movie_file:
    movie_id_to_index = json.load(movie_file)

def load_users(session):
    # do not use ratings.dat - just use indexes
    for user_id in user_id_to_index.iterkeys():
        user = model.User(int(user_id), None, None, None)
        session.add(user)
    session.commit()


def load_movies(session):
    # use movies.dat
    #1::Toy Story (1995)::Adventure|Animation|Children|Comedy|Fantasy

    with open("../data/ml-10M100K/movies.dat") as itemfile:
        for line in itemfile:
            line = line.split('::')
            title = line[1]
            title = title.decode("latin-1")
            movie_id = line[0]
            genre = line[2]
            genre = genre.decode("latin-1")
            item = model.Movie(movie_id_to_index[movie_id], title, genre)
            session.add(item)
        session.commit()


def load_ratings(session):
    # use ratings
    #1::120::5::838983396
    # user id :: movie id :: rating :: time
    # do index conversion
    i = 0
    datafile = open("../data/ml-10M100K/ratings.dat", "r")
    for line in datafile:
        line = line.split('::')
        rating = model.Rating(user_id_to_index[line[0]], movie_id_to_index[line[1]], line[2], line[3])
        session.add(rating)
        i += 1
        if i % 10000 == 0:
            session.commit()
    session.commit()
    datafile.close()

# use pypy to seed database (much faster), do it 1-by-1 to make sure everything loads
def main(session):
    print "Loading users"
    load_users(session)
    print "Loading movies"
    load_movies(session)
    print "Loading ratings"
    load_ratings(session)
    print "Done loading"

if __name__ == "__main__":
    s = model.connect()
    main(s)