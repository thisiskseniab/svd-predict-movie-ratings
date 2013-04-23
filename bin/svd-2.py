
try:
  import numpypy
except:
  pass

import numpy
import copy
import random


# I need foloowing operations with matricies:
# matrix.subtract(matrix) (minus?)
# matrix.multiply(coefficient) (times?)
# following defines what a matrix is and how to do operations with it
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


# start with a matrix of ratings
# how many users are there? how many movies? (put 5 for users and 10 for movies right now)
# find a way to iterate through movie ids & so they are connected to the actual ratings
def get_test_matrix():
  t = Matrix(4, 5, 0) #71567, 10681 139
  for x in range(t.width):
    for y in range(t.height):
      t.set(x, y, random.randrange(1, 5, 1))
  #t.values = [1,2,3,4,5] * 1000 #200010
  return t

def get_another_test_matrix():
  nmp = [[ 1., 3., 3., 4., 1.], [ 2., 2., 4., 3., 1.], [ 2., 3., 3., 3., 1.], [ 2., 3., 4., 4., 2.]]
  b = [[ 2.,  4.,  1.,  1.,  3.], [ 1.,  2.,  1.,  1.,  2.], [ 3.,  4.,  2.,  1.,  3.], [ 1.,  2.,  1.,  3.,  2.]]
  t = Matrix(4, 5, 0)
  t.matrix = numpy.array(b) # cheating!
  return t

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
    if count == 0:
      pass
    else:
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
  for x in range(ratings.width):
      r = ratings.index(x, movie)
      if r > 0:
        count += 1
  return count

def sum_of_observed_ratings(ratings, movie):
  total_sum = 0
  for x in range(ratings.width):
      r = ratings.index(x, movie)
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
  for x in range(ratings.width):
      r = ratings.index(x, movie)
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
  k = vb/va #25 ?
  betterMean = (global_average * k + sum_obs ) / ( k + count_obs )
  return betterMean


# the average offset between a user's rating and the movie's average rating
# we need: k = 25, average ratings of all movies (global average - mean of avg ratings)
# sum of user's ratings, count of user's ratings
def sum_of_user_ratings(ratings, user):
  total_sum = 0
  for x in range(ratings.width):
      r = ratings.index(user, x)
      if r > 0:
        total_sum += r
  return total_sum


def count_of_user_ratings(ratings, user):
  count = 0
  for x in range(ratings.width):
      r = ratings.index(user, x)
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
  for x in range(ratings.width):
      r = ratings.index(user, x)
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
  k = vb/va
  betterMean = ( global_average * k + sum_user ) / ( k + count_user )
  return betterMean


# NOW WE ARE PREDICTING A RATING WHOOOHOOO HA
# "Note that predictRating() here would also use userValue and movieValue to do its work,
# so there's a tight feedback loop in play."
# http://sifter.org/~simon/journal/20061211.html
# TODO: ^ figure out what this means, you'll probably have to pass the feature vectors in
#       so you can mutate them
def predict_rating(ratings, movie, user):
  # if ratings.index(user, movie) > 0:
  #   return ratings.index(user, movie)
  average_rating_mov = average_rating(ratings, movie)
  average_user_off = average_user_offset(ratings, user)
  predict_rating = (average_rating_mov + average_user_off) / 2
  return predict_rating


# def predict_rating(r, m, u):
#   return 3;


###EVERYTHING DOWN BELOW WORKS FOR REALZ, IF PROBLEMS MOST LIKELY IN PREDICT RATING AND STUFF ABOVE IT

initial = 0.1
lrate = 0.001

# was get_error_matrix
def multiply_feature_vectors(userFeature, movieFeature):
  result = Matrix(len(userFeature), len(movieFeature), 0)
  for w in range(result.width):
    for h in range(result.height):
      result.set(w, h, userFeature[w] * movieFeature[h])
  return result


def train_rating(real, user_index, movie_index, rating, userFeature, movieFeature):
  error = lrate * (rating - predict_rating(real, movie_index, user_index))
  uv = userFeature[user_index]
  userFeature[user_index] += error * movieFeature[movie_index]
  movieFeature[movie_index] += error * uv


def train_feature_vectors(real, remainder, userFeature, movieFeature):

  # build error matrix by predicting some ratings and subtracting from real
  predictions = multiply_feature_vectors(userFeature, movieFeature)
  # print predictions

  # subtract predicted values matrix from remainder to get errors
  errors = real.minus(predictions)
  # print errors

  # multiply error by the learning rate
  errors.times(lrate)
  # print errors

  # TRAIN THE RESULT to build new feature vector
  for x in range(errors.width):
    for y in range(errors.height):
      train_rating(real, x, y, errors.index(x, y), userFeature, movieFeature)

  #print multiply_feature_vectors(userFeature, movieFeature)

  # print error_matrix.dict
  #predicted_ratings = test_matrix.minus(error_matrix)
  # print error_matrix.dict
  # print predicted_ratings.dict
  return userFeature, movieFeature


# this comment is old \/
# call train_feature_vectors within a loop of 40 to do it for all 40 features
def train_all_features(real):

  userFeatureVectors = []
  movieFeatureVectors = []

  prior = real
  remainder = real #?
  for i in range(30):

    # get fresh feature vectors for each singular value we decompose from real
    uF, mF = init_feature_vectors(prior.width, prior.height)

    for j in range(10):


      uF, mF = train_feature_vectors(prior, remainder, uF, mF)

      prediction_based_on_singular_values = multiply_feature_vectors(uF, mF)
      print "prediction", prediction_based_on_singular_values

      remainder = prior.minus(prediction_based_on_singular_values)
      print "remainder", remainder

    prior = remainder

    userFeatureVectors.append(copy.copy(uF))
    movieFeatureVectors.append(copy.copy(mF))
    # print rm, uf, mf

  return userFeatureVectors, movieFeatureVectors


def init_feature_vectors(width, height):
  # set feature vectors to initial
  userFeature = [initial] * width
  movieFeature = [initial] * height
  return userFeature, movieFeature


def train_one_feature_our_way(real, sigma = 0.3):
  cycles = 0
  max_cycles = 600
  uF, mF = init_feature_vectors(real.width, real.height)
  while True:
    cycles += 1
    predicted = multiply_feature_vectors(uF, mF)
    errors = real.minus(predicted)
    if errors.mean() < sigma or cycles >= max_cycles:
      # we may want to have a max cycle
      #print cycles
      break
    else:
      errors.times(lrate)
      for w in range(real.width):
        for h in range(real.height):
          error = abs(lrate * (predicted.index(w, h) - predict_rating(real, h, w)))
          uv = uF[w]
          uF[w] += error * mF[h]
          mF[h] += error * uv
  return uF, mF


def train_some_features(real, feature_count):

  sigma = 0.8

  userFeatures = []
  movieFeatures = []
  remainder = real
  last_difference = 0

  for i in range(feature_count):
    uF, uM = train_one_feature_our_way(remainder, sigma)
    singular_value = multiply_feature_vectors(uF, uM)
    remainder = remainder.minus(singular_value)
    userFeatures.append(uF)
    movieFeatures.append(uM)
    sigma /= 4
    if abs(remainder.mean() - last_difference) < 0.01:
      break
    last_difference = remainder.mean()
    # if (real.mean() - remainder.mean()) < 0.8:
    #   break

  return userFeatures, movieFeatures


test_matrix = get_test_matrix()
#ufs, mfs = train_all_features(test_matrix)
#uF, mF = train_one_feature_our_way(test_matrix)

print test_matrix
#print multiply_feature_vectors(uF, mF)

uFs, mFs = train_some_features(test_matrix, 10)

for singular in range(len(uFs)):
  # print 'user feature vector '+ str(singular), uFs
  # print 'movie feature vector '+ str(singular), mFs
  singular_value = multiply_feature_vectors(uFs[singular], mFs[singular])
  print singular, singular_value
  print 'difference', test_matrix.minus(singular_value).mean()

another_test_matrix = get_another_test_matrix()
uF, mF = train_one_feature_our_way(another_test_matrix)

# print ufs[29]
# print mfs[29]
# print "prediction?", multiply_feature_vectors(ufs[29], mfs[29])




# error_matrix = multiply_feature_vectors(uf, mf)
# predicted_ratings = test_matrix.minus(error_matrix)

# predicted_rating = predict_rating(test_matrix, 2, 1)
# print test_matrix.dict
# print predicted_ratings.dict
# print uf, mf
# print error_matrix.dict
# print predicted_rating
# print test_matrix.dict



ratings = open('../data/ml-10M100K/ratings.dat')

for line in ratings:
  values = line.split('::') # todo fix me pls this is awful splitting twice wat

  userId = values[0]
  movieId = values[1]

  if not userId in users:
    users[userId] = User(userId)

  users[userId].add_rating(line, movieId)


# you want to count the movies
# count the users
# make arrays that map the movie ids -> movie indexes and user ids -> user indexes
# write a function that takes a rating and inserts it into a matrix at an appropriate point






