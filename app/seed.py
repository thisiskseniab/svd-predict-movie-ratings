import model
import csv
from datetime import datetime
import json

# All the paths for filenames in seed.py are relative to the project folder
# not the app/ directory, so i took '../' off the beginning

# get an id -> index json object for movies and users
with open('data/ml-10M100K/user_id_to_index.json', 'r') as user_file:
    user_id_to_index = json.load(user_file)

with open('data/ml-10M100K/movie_id_to_index.json', 'r') as movie_file:
    movie_id_to_index = json.load(movie_file)

def load_users(session):
    # do not use ratings.dat
    for user_id in user_id_to_index.iterkeys():
        user = model.User(int(user_id), None, None, None, None)
        session.add(user)
    session.commit()


def load_movies(session):
    # use matrix_movies.dat
    #0::1::Toy Story (1995)::Adventure|Animation|Children|Comedy|Fantasy

    with open("data/ml-10M100K/movies.dat") as itemfile:
        for line in itemfile:
            line = line.split('::')
            title = line[2]
            title = title.decode("latin-1")
            movie_id = line[0]
            item = model.Movie(movie_id_to_index[movie_id], title, line[3])
            session.add(item)
        session.commit()


def load_ratings(session):
    # use ratings
    #1::120::5::838983396
    # user id :: movie id :: rating :: time
    # do index conversion
    with open("data/ml-10M100K/ratings.dat") as datafile:
        for line in datafile:
            line = line.split('::')
            rating = model.Rating(user_id_to_index[line[0]], movie_id_to_index[line[1]], line[2], line[3])
            session.add(rating)
        session.commit()


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_ratings(session)
    load_movies(session)

if __name__ == "__main__":
    s = model.connect()
    main(s)