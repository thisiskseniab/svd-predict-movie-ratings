
# I need foloowing operations with matricies:
# matrix.subtract(matrix) (minus?)
# matrix.multiply(coefficient) (times?)
# following defines what a matrix is and how to do operations with it
import random

class Matrix:
  # set matrix in a dictionary to get rid of zeros
  def __init__(self, width, height, i):
    self.width = width
    self.height = height
    self.dict = {(x,y):i for x in range(width) for y in range(height)}

  # the index function will work like m[2, 3] and returns a value
  def index(self, x, y):
    return self.dict[x, y]

  def set(self, x, y, value):
    self.dict[x, y] = value
 
  # unlike times, minus will not alter self
  def minus(self, other_matrix):
    assert(self.width == other_matrix.width)
    assert(self.height == other_matrix.height)
    result = Matrix(self.width, self.height, 0)
    for x in range(self.width):
      for y in range(self.height):
        result.set(x, y, self.dict[x,y] - other_matrix.dict[x, y])
    return result

  # times multiplies all values by a coefficient
  def times(self, coefficient):    
    self.dict = {key:value*coefficient for key, value in self.dict.items()}
'''
def test_matrix_times():
  m = Matrix(2, 5, 2)
  cf = 5
  m.times(cf)
  assert(m.index(0,0) == 10)

def test_init():
  m = Matrix(2, 2, 3)
  assert(m.index(0,0) == 3)

def test_minus():
  m = Matrix(2, 2, 8)
  j = Matrix(2, 2, 3)
  r = m.minus(j)
  assert(r.index(0,0) == 5)

test_init()
test_matrix_times()
test_minus()
'''

# start with a matrix of ratings
# how many users are there? how many movies? (put 5 for users and 10 for movies right now)
# find a way to iterate through movie ids & so they are connected to the actual ratings 
def get_test_matrix():
  t = Matrix(10, 50, 0) #71567, 10681 139



  for x in range(t.width):
    for y in range(t.height):
      t.dict[x,y] = random.randrange(1, 5, 1)
  #t.values = [1,2,3,4,5] * 1000 #200010
  return t

initial = 0.1
lrate = 0.001

# users are width, movies are height
# this means movies are columns

# there are two kinds of variance we care about + mean
# * mean of average ratings of all movies
# * variance of average ratings of all movies
# * average variance of individual movie ratings (which tells you how indicative each new observation\
#is of the true mean)
def averages(ratings):
  averages = []
  for x in range(ratings.width):
    total = 0
    count = 0
    for y in range(ratings.height):
      r = ratings.index(x, y)
      if r > 0:
        total += r
        count += 1
      average = total / count 
      averages.append(average)
  return averages

def mean_of_avg_ratings(ratings):
  average = averages(ratings)
  #now find a mean - sum ov averages divided by number of averages
  mean = sum(average) / len(average)
  return mean

#now let's do it for individual movie:
def count_of_observed_ratings(ratings, movie):
  count = 0
  for y in range(ratings.height):
    if y == movie:
      for x in range(ratings.width):
          r = ratings.index(x, y)
          if r > 0:
            count += 1
  return count

def sum_of_observed_ratings(ratings, movie):
  total_sum = 0
  for y in range(ratings.height):
    if y == movie:
      for x in range(ratings.width):
          r = ratings.index(x, y)
          if r > 0:
            total_sum += r
  return total_sum


def mean_of_observed_ratings(ratings, movie):
  count = count_of_observed_ratings(ratings, movie)
  total_sum = sum_of_observed_ratings(ratings, movie)
  mean_of_movie = total_sum / count
  return mean_of_movie


def avg_variance_of_ind_movie_ratings(ratings, movie):
  mean_of_movie = mean_of_observed_ratings(ratings, movie)
  values = []
  #variance is a sum of squared differences between each value and a mean; divided by number of values
  for y in range(ratings.height):
    if y == movie:
      for x in range(ratings.width):
          r = ratings.index(x, y)
          d = (r-mean_of_movie)
          sq_d = d*d
          values.append(sq_d)
  variance = sum(values) / len(values)
  return variance

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
  return variance

#now find the good average rating for each movie
def average_rating(ratings, movie):
  bogusMean = mean_of_observed_ratings(ratings, movie)
  sum_obs = sum_of_observed_ratings(ratings, movie)
  count_obs = count_of_observed_ratings(ratings, movie)
  global_average = mean_of_avg_ratings(ratings)
  vb = avg_variance_of_ind_movie_ratings(ratings, movie)
  va = variance_of_avg_of_all_movies(ratings)
  k = 25 #vb/va ? 
  betterMean = (global_average * k + sum_obs ) / ( k + count_obs )
  return betterMean

# the average offset between a user's rating and the movie's average rating
# we need: k = 25, average ratings of all movies (global average - mean of avg ratings)
# sum of user's ratings, count of user's ratings
def sum_of_user_ratings(ratings, user):
  total_sum = 0
  for y in range(ratings.height):
    if y == user:
      for x in range(ratings.width):
          r = ratings.index(x, y)
          if r > 0:
            total_sum += r
  return total_sum

def count_of_user_ratings(ratings, user):
  count = 0
  for y in range(ratings.height):
    if y == user:
      for x in range(ratings.width):
          r = ratings.index(x, y)
          if r > 0:
            count += 1
  return count

def mean_of_user_ratings(ratings, user):
  count = count_of_user_ratings(ratings, user)
  total_sum = sum_of_user_ratings(ratings, user)
  mean_of_user = total_sum / count
  return mean_of_user

def avg_variance_of_ind_user_ratings(ratings, user):
  mean_of_user = mean_of_user_ratings(ratings, user)
  values = []
  #variance is a sum of squared differences between each value and a mean; divided by number of values
  for y in range(ratings.height):
    if y == user:
      for x in range(ratings.width):
          r = ratings.index(x, y)
          d = (r-mean_of_user)
          sq_d = d*d
          values.append(sq_d)
  variance = sum(values) / len(values)
  return variance

def average_user_offset(ratings, user):
  sum_user = sum_of_observed_ratings(ratings, user)
  count_user = count_of_user_ratings(ratings, user)
  global_average = mean_of_avg_ratings(ratings)
  vb = avg_variance_of_ind_user_ratings(ratings, user)
  va = variance_of_avg_of_all_movies(ratings)
  k = 25 #vb/va
  betterMean = ( global_average * k + sum_user ) / ( k + count_user )
  return betterMean

# NOW WE ARE PREDICTING A RATING WHOOOHOOO HA
def predict_rating(ratings, movie, user):
  average_rating_mov = average_rating(ratings, movie)
  average_user_off = average_user_offset(ratings, user)
  predict_rating = average_rating_mov + average_user_off
  return predict_rating

###EVERYTHING DOWN BELOW WORKS FOR REALZ, IF PROBLEMS MOST LIKELY IN PREDICT RATING AND STUFF ABOVE IT
def train_rating(ratings, user_index, movie_index, rating, userFeature, movieFeature):
  error = lrate * (rating - predict_rating(ratings, movie_index, user_index))
  uv = userFeature[user_index]
  userFeature[user_index] += error * movieFeature[movie_index]
  movieFeature[movie_index] += error * uv


def train_first_feature(real):
  # set feature vector to initial
  userFeature = [initial] * real.width
  movieFeature = [initial] * real.height
  # uf_mf_dict = {(x,y):userFeature*movieFeature for x in range(real.height) for y in range(real.width)}
  return train_all_features(real, real, userFeature, movieFeature)#train_all_features(real, real, userFeature, movieFeature)


def get_error_matrix(userFeature, movieFeature):
  width = len(userFeature)
  height = len(movieFeature)
  error_matrix = Matrix(width, height, 0)
  for x in range(error_matrix.width):
    for y in range(error_matrix.height):
      error_matrix.set(x, y, userFeature[x] * movieFeature[y])
  return error_matrix


def train_feature_vectors(real, remainder, userFeature, movieFeature):

  # build initial error matrix
  error_matrix = Matrix(remainder.width, remainder.height, 0)
  for x in range(error_matrix.width):
    for y in range(error_matrix.height):
      error_matrix.set(x, y, userFeature[x] * movieFeature[y])
  # print error_matrix.dict
  # subtract error matrix from real
  result = remainder.minus(error_matrix)

  # multiply result by the learning rate
  result.times(lrate)

  # TRAIN THE RESULT to build new feature vector
  for x in range(result.width):
    for y in range(result.height):
      train_rating(real, x, y, result.dict[x, y], userFeature, movieFeature)

  error_matrix = get_error_matrix(userFeature, movieFeature)
  # print error_matrix.dict
  predicted_ratings = test_matrix.minus(error_matrix)
  # print error_matrix.dict
  # print predicted_ratings.dict
  return error_matrix, userFeature, movieFeature

# call train_feature_vectors within a loop of 40 to do it for all 40 features
def train_all_features(real, remainder, userFeature, movieFeature):
  for i in range(40):
    eM, uF, mF = train_feature_vectors(real, remainder, userFeature, movieFeature)
    em, uf, mf = train_feature_vectors(real, eM, uF, mF)
    # print em.dict
    # print rm, uf, mf
  return uF, mF



test_matrix = get_test_matrix()
uf, mf = train_first_feature(test_matrix)
# error_matrix = get_error_matrix(uf, mf)
# predicted_ratings = test_matrix.minus(error_matrix)

# predicted_rating = predict_rating(test_matrix, 2, 1)
# print test_matrix.dict
# print predicted_ratings.dict
# print uf, mf
# print error_matrix.dict
# print predicted_rating
# print test_matrix.dict
