
try:
  import numpypy
except:
  pass

import numpy
import copy
import random

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
  def mean_axis(self, i):
    return self.matrix.mean(axis=i)


def get_test_matrix():
  t = Matrix(10000, 1500, 0) #71567, 10681 139
  for x in range(t.width):
    for y in range(t.height):
      t.set(x, y, random.randrange(1, 5, 1))
  #t.values = [1,2,3,4,5] * 1000 #200010
  return t

def get_another_test_matrix():
  nmp = [[ 1., 3., 3., 4., 1.], [ 2., 2., 4., 3., 1.], [ 2., 3., 3., 3., 1.], [ 2., 3., 4., 4., 2.]]
  b = [[ 1.,  0.,  0.,  0.,  0.], [ 0.,  1.,  0.,  0.,  0.], [ 1.,  0.,  0.,  0.,  0.], [ 0.,  0.,  0.,  0.,  0.]]
  t = Matrix(4, 5, 0)
  t.matrix = numpy.array(b) # cheating!
  return t

#WORKS!!!
def averages(ratings):
  # averages = ratings.mean()
  # print averages
  averages = []
  for h in range(ratings.height):
    total = 0
    count = 0
    for w in range(ratings.width):
      r = ratings.index(w, h)
      if r > 0:
        total += r
        count += 1
    if count == 0:
      pass
    else:
      average = total / count
      averages.append(average)
  # print averages
  return averages

#WORKS
def mean_of_avg_ratings(ratings):
  average = averages(ratings)
  # print average
  #now find a mean - sum ov averages divided by number of averages
  mean = sum(average) / len(average)
  # print mean
  return mean

#WORKS
#now let's do it for individual movie:
def count_of_observed_ratings(ratings, movie):
  count = 0
  for w in range(ratings.width):
      r = ratings.index(w, movie)
      if r > 0:
        count += 1
  # print count
  return count

#WORKS
def sum_of_observed_ratings(ratings, movie):
  total_sum = 0
  for w in range(ratings.width):
      r = ratings.index(w, movie)
      if r > 0:
        total_sum += r
  # print total_sum
  return total_sum

#WORKS
def mean_of_observed_ratings(ratings, movie):
  count = count_of_observed_ratings(ratings, movie)
  total_sum = sum_of_observed_ratings(ratings, movie)
  mean_of_movie = total_sum / count
  # print mean_of_movie
  return mean_of_movie

#SEEMS TO BE WORKING
def avg_variance_of_ind_movie_ratings(ratings, movie):
  mean_of_movie = mean_of_observed_ratings(ratings, movie)
  values = []
  #variance is a sum of squared differences between each value and a mean; divided by number of values
  for w in range(ratings.width):
      r = ratings.index(w, movie)
      d = (r-mean_of_movie)
      sq_d = d*d
      values.append(sq_d)
  variance = sum(values) / len(values)
  # print variance
  return variance

#SEEMS TO BE WORKING BUT NUMBER TURNS OUT VERY SMALL (0.19)
def variance_of_avg_of_all_movies(ratings):
  #here variance is a sum of squared differences between averages and a mean, divided by number of averages
  mean = mean_of_avg_ratings(ratings)
  average = averages(ratings)
  diffs = []
  for av in average:
    diff = (av - mean)
    sq_diff = diff * diff
    diffs.append(sq_diff)
  variance = sum(diffs) / len(diffs)
  # print variance
  return variance

#SEEMS TO BE WORKING
#now find the good average rating for each movie
def average_rating(ratings, movie):
  bogusMean = mean_of_observed_ratings(ratings, movie)
  sum_obs = sum_of_observed_ratings(ratings, movie)
  count_obs = count_of_observed_ratings(ratings, movie)
  global_average = mean_of_avg_ratings(ratings)
  vb = avg_variance_of_ind_movie_ratings(ratings, movie)
  va = variance_of_avg_of_all_movies(ratings)
  k = vb/va #25 ?
  # print global_average
  # print 'vb', vb
  # print va
  # print k
  # print sum_obs
  # print count_obs
  betterMean = ((global_average * k) + sum_obs ) / ( k + count_obs )
  print "movie mean", betterMean
  return betterMean


# the average offset between a user's rating and the movie's average rating
# we need: k = 25, average ratings of all movies (global average - mean of avg ratings)
# sum of user's ratings, count of user's ratings
#WORKS
def sum_of_user_ratings(ratings, user):
  total_sum = 0
  for h in range(ratings.height):
      r = ratings.index(user, h)
      if r > 0:
        total_sum += r
  # print total_sum
  return total_sum

#WORKS
def count_of_user_ratings(ratings, user):
  count = 0
  for h in range(ratings.height):
      r = ratings.index(user, h)
      if r > 0:
        count += 1
  # print count
  return count

#WORKS
def mean_of_user_ratings(ratings, user):
  # mean_of_user = ratings.mean_axis(user)
  count = count_of_user_ratings(ratings, user)
  total_sum = sum_of_user_ratings(ratings, user)
  mean_of_user = total_sum / count
  # print mean_of_user
  return mean_of_user

#WORKS
def avg_variance_of_ind_user_ratings(ratings, user):
  mean_of_user = mean_of_user_ratings(ratings, user)
  # print mean_of_user
  values = []
  #variance is a sum of squared differences between each value and a mean; divided by number of values
  for h in range(ratings.height):
      r = ratings.index(user, h)
      # print r
      d = (r-mean_of_user)
      # print d
      sq_d = d*d
      values.append(sq_d)
  # print values
  variance = sum(values) / len(values)
  # print variance
  return variance

#NO WORK NO WORK NO WORK
# what is an offset? it's the average difference between the actual average rating and the user's rating
# user's rating - average
def average_user_offset(ratings, user):
  sum_user = sum_of_observed_ratings(ratings, user)
  count_user = count_of_user_ratings(ratings, user)
  global_average = mean_of_avg_ratings(ratings)
  vb = avg_variance_of_ind_user_ratings(ratings, user)
  va = variance_of_avg_of_all_movies(ratings)
  k = vb/va
  # print 'k', k
  betterOffset = ( (global_average * k) + sum_user ) / ( k + count_user )
  print 'user offset', betterOffset
  return betterOffset


# NOW WE ARE PREDICTING A RATING WHOOOHOOO HA
# "Note that predictRating() here would also use userValue and movieValue to do its work,
# so there's a tight feedback loop in play."
# http://sifter.org/~simon/journal/20061211.html
# TODO: ^ figure out what this means, you'll probably have to pass the feature vectors in
#       so you can mutate them
def predict_rating(ratings, movie, user):
  average_rating_mov = average_rating(ratings, movie)
  average_user_off = average_user_offset(ratings, user)
  predict_rating = (average_rating_mov + average_user_off) 
  print predict_rating
  return predict_rating

test_matrix = get_test_matrix()
print test_matrix
# averages(test_matrix)
# mean_of_avg_ratings(test_matrix)
# sum_of_observed_ratings(test_matrix, 0)
# count_of_observed_ratings(test_matrix, 0)
# mean_of_user_ratings(test_matrix, 0)
# # mean_of_observed_ratings(test_matrix, 0)
# avg_variance_of_ind_movie_ratings(test_matrix, 0)
# variance_of_avg_of_all_movies(test_matrix)
# average_rating(test_matrix,0)
# avg_variance_of_ind_user_ratings(test_matrix, 0)
# sum_of_user_ratings(test_matrix, 0)
# count_of_user_ratings(test_matrix, 0)
# mean_of_user_ratings(test_matrix, 0)
# average_user_offset(test_matrix, 0)
predict_rating(test_matrix, 0, 0)
