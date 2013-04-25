try:
  import numpypy
except:
  pass
import numpy
import copy
import random
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

# UserId::MovieId::Rating::Timestamp
# ['30', '590', '5', '876529220']

# 0::1::Toy Story (1995)::Adventure|Animation|Children|Comedy|Fantasy

def main():
  ratings = open('../data/ml-10M100K/ratings.dat')
  movies = open('../data/ml-10M100K/matrix_movies.dat')
  mapped_ratings = {}
  # for x, y in [(x,y) for x in a for y in b]:
  for line2, line in product(movies, ratings):
    movies_values = line2.split('::')
    # for line in ratings:
    ratings_values = line.split('::')
    # print 'ratings', ratings_values
    # print 'movies', movies_values
    if ratings_values[1] == movies_values[1]:
      # print 'ratings value', ratings_values[1]
      # print 'movie value', movies_values[1]
      mapped_ratings[(int(ratings_values[0]),int(movies_values[0]))] = float(ratings_values[2])

  val_ratings = mapped_ratings.values()


  t = Matrix(71568, 10681, 0) #71567, 10681
  for key, value in mapped_ratings.iteritems():
    # print 'key1', key[0]
    # print 'key2', key[1]
    # print 'value', value
    t.set(key[0], key[1], value)
  # for value in val_ratings:
  #   print value
  #   for user in users:
  #     print user
  #     for movie in movies:
  #       print movie
  #       t.set(user, movie, value)
  outfile = TemporaryFile()
  np.save(outfile, t)

  savetxt('test_matrix.txt', t)

  # file = open('test_matrix.txt', 'w')
  # file.write(str(t))
  # file.close


if __name__ == "__main__":  
  main()


# i want to count the movies
# count the users
# make arrays that map the movie ids -> movie indexes and user ids -> user indexes
# write a function that takes a rating and inserts it into a matrix at an appropriate point