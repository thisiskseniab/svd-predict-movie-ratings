import model
import csv
from datetime import datetime

def load_users(session):
    # use ratings.dat

    with open("../data/ml-10M100K/ratings.dat") as userfile:
        userreader = csv.reader(userfile, delimiter="::")
        for line in userreader:
            if line[0] not in session:
                user = model.User(line[0], None, None, None, None)
                session.add(user)
        session.commit() 

def load_movies(session):
    # use matrix_movies.dat
    #0::1::Toy Story (1995)::Adventure|Animation|Children|Comedy|Fantasy

    with open("../data/ml-10M100K/matrix_movies") as itemfile:
        itemreader = csv.reader(itemfile, delimiter="::")
        for line in itemreader:
            title = line[2]
            title = title.decode("latin-1")
            item = model.Movies(title, line[3])
            session.add(item)
        session.commit() 

def load_ratings(session):
    # use ratings
    #1::120::5::838983396

    with open("seed_data/u.data") as datafile:
        datareader = csv.reader(datafile, delimiter="::")
        for line in datareader:
            rating = model.Ratings(line[0], line[1], line[2], line[3])
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
