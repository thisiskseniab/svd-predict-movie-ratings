
try:
  import numpypy
except:
  pass

import numpy
import random
import time

import json

class Matrix:
    def __init__(self, width, height, i):
        self.width = width
        self.height = height
        self.matrix = numpy.zeros([width, height], dtype='float32')
        self.matrix.fill(i)
    def __str__(self):
        return self.matrix.__str__()
    def index(self, w, h):
        return self.matrix[w][h]
    def set(self, w, h, value):
        self.matrix[w, h] = value
    def minus(self, other):
        return DifferenceMatrix(self, other)

class VectorProductMatrix:
    # user first, then movie
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.width = len(v1)
        self.height = len(v2)
    def __str__(self):
        return str(get_real_matrix(self))
    def index(self, w, h):
        return self.v1[w] * self.v2[h]
    # this actually makes sense
    def minus(self, other):
        return DifferenceMatrix(self, other)

class DifferenceMatrix:
    def __init__(self, remainder, featureMatrix):
        self.remainder = remainder
        self.featureMatrix = featureMatrix
        self.width = remainder.width
        self.height = remainder.height
    def __str__(self):
        return str(get_real_matrix(self))
    def index(self, w, h):
        return self.remainder.index(w, h) - self.featureMatrix.index(w, h)
    def minus(self, other):
        return DifferenceMatrix(self, other)
        

def get_real_matrix(unreal):
    result = Matrix(unreal.width, unreal.height, 0)
    for w in xrange(unreal.width):
        for h in xrange(unreal.height):
            result.set(w, h, unreal.index(w, h))
    return result


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

initial = 0.3
lrate = 0.01

# was get_error_matrix
def multiply_feature_vectors(userFeature, movieFeature):
    return VectorProductMatrix(userFeature, movieFeature)

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
    max_cycles = 25
    print "initializing feature vectors"
    uF, mF = init_feature_vectors(real.width, real.height)
    last = time.time()
    while True:
        cycles += 1
        print 'cycles of training one vector', cycles
        if cycles == max_cycles: #errors.mean() < sigma or
            break
        else:
            # WHY DOES THIS LOOP TAKE FOREVER? 
            # 68878 * 10680 * 8 operations = ~5 billion operations my processor - 2.8 Ghz ~ 2.8 billion operations per second
            for w in xrange(real.width): #69878
                if w % 10000 == 0:
                    print time.time() - last
                    print 'users w, cycles', w, cycles
                    last = time.time()
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
        print "writing user vector", iteration
        uf1 = json.dumps(uF)
        with open('feature'+ str(i) +'_vector_user.json', 'a') as f:
            f.write(uf1)
            f.write('\n')
        print "writing movie vector", iteration
        mf1 = json.dumps(uF)
        with open('feature'+ str(i) +'_vector_movie.json', 'a') as p:
            p.write(mf1)
            p.write('\n')
        # print "appending user features to list of vectors"
        userFeatures.append(uF)
        # print "appending movie features to list of vecors"
        movieFeatures.append(uM)
        # print "calculating singular value by multiplying feature vectors"
        singular_value = multiply_feature_vectors(uF, uM)
        # print "calculating ramainder (remainder minus singular_value"
        remainder = remainder.minus(singular_value)
        iteration += 1
        print "trained vector #", iteration
    return userFeatures, movieFeatures
    

# test_matrix = get_another_test_matrix()
print "setting matrix"
test_matrix = set_matrix_with_real_data()

print "doing svd"
uFs, mFs = train_some_features(test_matrix, 5)


print "loading to json"
print "loading user vector"
uf = json.dumps(uFs)
print "loading movie vector"
mf = json.dumps(mFs)
print "writing user vector"
f = open('feature_vector_user_all.json', 'w')
f.write(uf)
f.close
print "writing movie vector"
p = open('feature_vector_movie_all.json', 'w')
p.write(mf)
p.close 

# for singular in range(len(uFs)):
#   print 'user feature vector '+ str(singular), uFs[singular]
#   print 'movie feature vector '+ str(singular), mFs[singular]
#   singular_value = multiply_feature_vectors(uFs[singular], mFs[singular])
#   print singular, singular_value





