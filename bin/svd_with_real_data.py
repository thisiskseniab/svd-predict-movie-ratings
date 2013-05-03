
try:
  import numpypy
except:
  pass

import numpy
import copy
import random

import json

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
    # this method seems really slow
    def load_from_redis(self):
        for user_index in xrange(self.width):
          for movie_index in xrange(self.height):
            rating = redis_server.get(user_movie_key(user_index, movie_index))
            if rating > 0:
              self.set(user_index, movie_index, rating)

class UnrealizedMatrix:
    # def __init__(self):
    #     pass
    def __init__(self, featurevector1, featurevector2):
        self.featurevector1 = featurevector1
        self.featurevector2 = featurevector2 
    def index_multiply(self, user_index, movie_index):
        return self.featurevector1[user_index] * self.featurevector2[movie_index]

    def index_minus(self, user_index, movie_index, real):
        result = (self.featurevector1[user_index] * self.featurevector2[movie_index]) - real.index(user_index, movie_index)
        return result

    def index_times(self, user_index, movie_index, coefficient):
        result = self.featurevector1[user_index] * self.featurevector2[movie_index] * coefficient
        return result
        

# redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)

# # vector_type is either 'user' or 'movie'
def write_feature_vector_to_redis(vector_type, feature_number, feature_vector):
    key = 'feature_vector:' + vector_type + ':' + feature_number
    for index in xrange(len(feature_vector)):
        redis_server.zadd(key, index, feature_vector[index])

# deliver a user's predicted ratings from all feature vectors in redis
# get predictions for a user from redis
def get_user_predicted_values(user_index):
    user_predictions = {} # movie_index -> rating
    user_predictions.set_default(0)
    movie_feature_vector_keys = redis_server.keys('feature_vector:movie:*')
    for feature_index in xrange(len(movie_feature_vector_keys)):
        user_feature_value = redis_server.zrangebyscore('feature_vector:user:' + feature_index, user_index, user_index)
        movie_feature_vector = redis_server.zrangebyscore('feature_vector:movie:' + feature_index, 0, 'inf')
        for movie_index in xrange(len(movie_feature_vector)):
            prediction_matrix = getUnrealMatrix(user_feature_value, movie_feature_vector)
            prediction = prediction_matrix.index(user_index, movie_index)
    return prediction

#get predicted ratings from redis vectors
def get_user_predicted_ratings(user_index):
    user_predictions = {} # movie_index -> rating
    user_predictions.set_default(0)
    movie_feature_vector_keys = redis_server.keys('feature_vector:movie:*')
    for feature_index in xrange(len(movie_feature_vector_keys)):
        user_feature_value = redis_server.zrangebyscore('feature_vector:user:' + feature_index, user_index, user_index)
        movie_feature_vector = redis_server.zrangebyscore('feature_vector:movie:' + feature_index, 0, 'inf')

def predict_rating(user, userFeature, movieFeature):
    pass


# loads a matrix from redis
def load_original_values_from_redis():
    user_count = 69878
    movie_count = 10681
    ratings_matrix = Matrix(user_count, movie_count, 0) #69878, 10681
    ratings_matrix.load_from_redis()
    return ratings_matrix


def get_test_matrix():
    t = Matrix(100, 50, 0) #71567, 10681 139
    for x in range(t.width):
        for y in range(t.height):
            t.set(x, y, 3) #random.randrange(1, 5, 1))
    #t.values = [1,2,3,4,5] * 1000 #200010
    return t

def get_another_test_matrix():
    nmp = [[ 1., 5., 2., 5., 4.], [ 0., 3., 5., 4., 2.], [ 1., 5., 3., 3., 1.], [ 2., 3., 4., 4., 2.]]
    b = [[ 2.,  4.,  1.,  1.,  3.], [ 1.,  2.,  1.,  1.,  2.], [ 3.,  4.,  2.,  1.,  3.], [ 1.,  2.,  1.,  3.,  2.]]
    threes = [[ 3., 3., 3., 3., 3.], [ 3., 3., 3., 3., 3.], [ 3., 3., 3., 3., 3.], [ 3., 3., 3., 3., 3.]]
    t = Matrix(4, 5, 0)
    t.matrix = numpy.array(threes) # cheating!
    return t

#sets a matrix with real data from original file
def set_matrix_with_real_data():
    with open('../data/ml-10M100K/user_id_to_index.json', 'r') as user_file:
        user_index = json.load(user_file)

    with open('../data/ml-10M100K/movie_id_to_index.json', 'r') as movie_file:
        movie_index = json.load(movie_file)

    user_count = 69878
    movie_count = 10681
    ratings_matrix = Matrix(user_count, movie_count, 0) #69878, 10681
    ratings_file = open('../data/ml-10M100K/ratings.dat')
    for line in ratings_file:
        user_id = line.split('::')[0]
        movie_id = line.split('::')[1]
        rating =  line.split('::')[2]
        ratings_matrix.set(user_index[user_id], movie_index[movie_id], rating)
    return ratings_matrix

initial = 0.1
lrate = 0.001

# was get_error_matrix
def multiply_feature_vectors(userFeature, movieFeature):
    print "setting a matrix of new feature vectors"
    result = Matrix(len(userFeature), len(movieFeature), 0)
    print "looping through the lenght of both vectors"
    for w in xrange(result.width):
        for h in xrange(result.height):
            print "multiplying vectors at point", w, h
            result.set(w, h, userFeature[w] * movieFeature[h])
    return result

def init_feature_vectors(width, height):
    # set feature vectors to initial
    userFeature = [initial] * width
    movieFeature = [initial] * height
    return userFeature, movieFeature

#train one feature using svd formula
#error = (original rating - product of vectors)*lrate
#userfeature += error * moviefeature
#moviefeature += eroor * userfeature
def train_one_feature(real): #, sigma = 0.01):
    cycles = 0
    max_cycles = 400
    print "initializing feature vectors"
    uF, mF = init_feature_vectors(real.width, real.height)
    while True:
        cycles += 1
        print 'cycles of training one vector', cycles
        if cycles == max_cycles: #errors.mean() < sigma or
            break
        else:
            # WHY DOES THIS LOOP TAKE FOREVER? 
            # 68878 * 10680 * 8 operations = ~5 billion operations my processor - 2.8 Ghz ~ 2.8 billion operations per second
            j = 0
            for w in xrange(real.width): #69878
                if w % 1000 == 0:
                    print 'users w, movies h, cycles', w, h, cycles
                for h in xrange(real.height): #10681
                #I thought that error has to be an absolute value, but it was throwing the results off
                #increasing the vectors all the time instead of correcting values of vectors
                    predicted_w_h = uF[w] * mF[h] #don't need to set up the whole matrix here, just do it on the spot
                    error = (real.index(w, h) - predicted_w_h) * lrate 
                    uv = uF[w]
                    uF[w] += error * mF[h]
                    mF[h] += error * uv
                
    return uF, mF


#train as many features as necessary by calling one feature function
#consider adding a sigma to automate features production
def train_some_features(real, feature_count):
    # sigma = 5.0
    userFeatures = []
    movieFeatures = []
    remainder = real
    iteration = 0
    for i in xrange(feature_count):
        uF, uM = train_one_feature(remainder) #, sigma)
        # print "writing user vector", cycles
        # uf1 = json.dumps(uF)
        # with open('feature_vector_user.json', 'a') as f:
        #     f.write(uf1)
        # print "writing movie vector", cycles
        # mf1 = json.dumps(uF)
        # with open('feature_vector_movie.json', 'a') as p:
        #     p.write(mf1)
        print "appending user features to list of vectors"
        userFeatures.append(uF)
        print "appending movie features to list of vecors"
        movieFeatures.append(uM)
        print "calculating singular value by multiplying feature vectors"
        singular_value = multiply_feature_vectors(uF, uM)
        print "calculating ramainder (remainder minus singular_value"
        remainder = remainder.minus(singular_value)
        # iteration += 1
        # print "trained vector #", iteration
    return userFeatures, movieFeatures
    

test_matrix = get_another_test_matrix()
print "setting matrix"
# test_matrix = set_matrix_with_real_data()

print "doing svd"
uFs, mFs = train_some_features(test_matrix, 2)


# print "loading to json"
# print "loading user vector"
# uf = json.dumps(uFs)
# print "loading movie vector"
# mf = json.dumps(mFs)
# print "writing user vector"
# f = open('feature_vector_user_all.json', 'w')
# f.write(uf)
# f.close
# print "writing movie vector"
# p = open('feature_vector_movie_all.json', 'w')
# p.write(mf)
# p.close 

# print "loading to redis"
# for vector_index in xrange(len(uFs)):   
#   write_feature_vector_to_redis('user', uFs[vector_index], vector_index)

# for vector_index in xrange(len(mFs)):
#   write_feature_vector_to_redis('movie', mFs[vector_index], vector_index)


# file.write('\noriginal matrix' + '\n' + str(test_matrix))
# for singular in range(len(uFs)):
#   print 'user feature vector '+ str(singular), uFs[singular]
#   print 'movie feature vector '+ str(singular), mFs[singular]
#   singular_value = multiply_feature_vectors(uFs[singular], mFs[singular])
#   print singular, singular_value
  # file.write('\n'+ str(singular))
  # file.write('\nuser feature vector ' + '\n' + str(uFs[singular]))
  # file.write('\nmovie feature vector '+ '\n' + str(mFs[singular]))
  # file.write('\nsingular value ' + '\n' + str(singular_value))
  # file.write('\n')
  # diff = test_matrix.minus(singular_value).mean()
  # file.write('\ndifference' + str(diff))
  # print 'difference', diff

# file.close()

#minimized function calls
#had sigma that was unnecessary (?)
#numpy matrix takes much less memory than anything else

