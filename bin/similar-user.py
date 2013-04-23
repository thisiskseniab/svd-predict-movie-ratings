#! /usr/bin/env pypy

# UserID::MovieID::Rating::Timestamp
# 1::122::5::838985046

class Rating:
  def __init__(self, line):
    values = line.split('::')
    self.userId = values[0]
    self.movieId = values[1]
    self.rating = values[2]
    self.timestamp = values[3]

class User:
  def __init__(self, id):
    self.id = id
    self.ratings = {} # movie id -> rating object

  def add_rating(self, line, movieId):
    self.ratings[movieId] = Rating(line)


users = {} # user id -> user object

# for each line of the file
# if the user exists, add the rating line to the user object
# otherwise create the user object and add the rating line to it
def main():
  ratings = open('../data/ml-10M100K/ratings_25.dat')


  for line in ratings:
    print line
    values = line.split('::')
    print values

    # userId = values[0]
    # movieId = values[1]

    # if not userId in users:
    #   users[userId] = User(userId)

    # users[userId].add_rating(line, movieId)



if __name__ == "__main__":  
  main()






