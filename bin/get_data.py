try:
  import numpypy
except:
  pass

import numpy
import copy
import random

import json

# reduce the precision of floating point
# from json import encoder
# encoder.FLOAT_REPR = lambda o: format(o, '.12g')

import redis

from itertools import product
from tempfile import TemporaryFile


class Matrix:
  def __init__(self, width, height, i):
    self.width = width
    self.height = height
    self.matrix = numpy.zeros([width, height], dtype='float32')
    self.matrix.fill(i)
  def index(self, w, h):
    return self.matrix[w][h]
  def set(self, w, h, value):
    self.matrix[w, h] = value
  def minus(self, other):
    result = Matrix(self.width, self.height, 0)
    result.matrix = self.matrix - other.matrix
    return result
  def times(self, coefficient):
    self.matrix = self.matrix * coefficient
  def __str__(self):
    return self.matrix.__str__()
  def mean(self):
    return self.matrix.mean()
  # this method seems pretty slow
  def load_from_redis(self):
    for user_index in xrange(self.width):
      for movie_index in xrange(self.height):
        rating = redis_server.get(user_movie_key(user_index, movie_index))
        if rating > 0:
          self.set(user_index, movie_index, rating)


# RULE: user first and then movie

def user_movie_key(user_index, movie_index):
  return 'user,movie:' + ','.join([str(user_index), str(movie_index)])


redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)

# this method does one redis write per rating, takes 700s for the original matrix
def save_rating_to_redis(user_index, movie_index, rating):
  redis_server.set('user,movie:' + ','.join([str(user_index), str(movie_index)]), rating)


# this method does one redis write per user,
# this seems strangely slower than the one-write-per-rating
def save_all_users_ratings_to_redis(matrix):
  user_count = matrix.width
  movie_count = matrix.height
  for user_index in range(user_count):
    # make a new dictionary for each user
    user_ratings = {}
    for movie_index in range(movie_count):
      rating = matrix.index(user_index, movie_index)
      if rating > 0:
        user_ratings[movie_index] = rating.tolist() # numpy hack to fix numeric type

    redis_server.set('user:'+ str(user_index), json.dumps(user_ratings))


# UserId::MovieId::Rating::Timestamp
# ['30', '590', '5', '876529220']

# 0::1::Toy Story (1995)::Adventure|Animation|Children|Comedy|Fantasy

def load_file_into_redis():
  # ratings = open('../data/ml-10M100K/new_ratings.dat')
  # mapped_ratings = {}
  # # for x, y in [(x,y) for x in a for y in b]:
  # for line in ratings:
  #   ratings_values = line.split('::')
  #   # print 'ratings', ratings_values
  #   mapped_ratings[(int(ratings_values[0]),int(ratings_values[1]))] = float(ratings_values[2])

  # val_ratings = mapped_ratings.values()

  with open('../data/ml-10M100K/user_id_to_index.json', 'r') as user_file:
    user_index = json.load(user_file)

  with open('../data/ml-10M100K/movie_id_to_index.json', 'r') as movie_file:
    movie_index = json.load(movie_file)

  # users are width?
  # movies are height?
  user_count = 69878
  movie_count = 10681
  ratings_matrix = Matrix(user_count, movie_count, 0) #69878, 10681
  ratings_file = open('../data/ml-10M100K/ratings.dat')

  print "Loading file and writing to Redis"
  for line in ratings_file:
    user_id = line.split('::')[0]
    movie_id = line.split('::')[1]
    rating =  line.split('::')[2]
    ratings_matrix.set(user_index[user_id], movie_index[movie_id], rating)
    save_rating_to_redis(user_index[user_id], movie_index[movie_id], rating)

  #save_all_users_ratings_to_redis(ratings_matrix)

  print "Reading matrix from Redis"
  ratings_matrix = Matrix(user_count, movie_count, 0) #71567, 10681
  ratings_matrix.load_from_redis()

  # outfile = TemporaryFile(prefix='ratings-tmp')
  # numpy.save(outfile, ratings_matrix)
  # outfile.write(str(ratings_matrix))
  # outfile.close()
  # numpy.savetxt('test_matrix.txt', ratings_matrix)







if __name__ == "__main__":
  load_file_into_redis()

#challenge: numpy doesn't support writing large data
