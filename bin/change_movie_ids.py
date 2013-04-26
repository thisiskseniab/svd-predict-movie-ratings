try:
  import numpypy
except:
  pass
import numpy

from itertools import product

ratings = open('../data/ml-10M100K/ratings.dat')
movies = open('../data/ml-10M100K/matrix_movies.dat')
new_ratings = open('../data/ml-10M100K/ratings_new.dat', 'w')
for line2, line in product(movies, ratings):
    movies_values = line2.split('::')
    # print movies_values
    ratings_values = line.split('::')
    # print ratings_values
    if movies_values[1] == ratings_values[1]:
    	# print movies_values[1]
    	# print ratings_values[1]
    	new_ratings.write(str(ratings_values[0]) + '::' + str(movies_values[0]) + '::' + str(ratings_values[2]) + '::' + str(ratings_values[3]))

movies.close()
ratings.close()
new_ratings.close()