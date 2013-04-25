
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
  

def get_test_matrix():
  t = Matrix(10000, 5000, 0) #71567, 10681 139
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

def unpack_matrix_from_text_file():
  matrix = genfromtxt('test_matrix.txt', unpack=True)
  return matrix

def unpack_matrix_from_npy_file():
  matrix = numpy.load('outfile.npy')
  return matrix
# users are width movies are height
# this means movies are columns

initial = 0.1
lrate = 0.001

# was get_error_matrix
def multiply_feature_vectors(userFeature, movieFeature):
  result = Matrix(len(userFeature), len(movieFeature), 0)
  for w in range(result.width):
    for h in range(result.height):
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
def train_one_feature(real): #sigma = 0.01
  cycles = 0
  max_cycles = 600
  uF, mF = init_feature_vectors(real.width, real.height)
  while True:
    cycles += 1
    predicted = multiply_feature_vectors(uF, mF)
    if cycles == max_cycles: #errors.mean() < sigma or 
      break
    else:
      for w in range(real.width):
        for h in range(real.height):
          #I thought that error has to be an absolute value, but it was throwing the results off 
          #increasing the vectors all the time instead of correcting values of vectors 
          error = (real.index(w, h) - predicted.index(w, h)) * lrate 
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
  last_difference = 0
  iteration = 0
  for i in range(feature_count):
    uF, uM = train_one_feature(remainder) #, sigma
    userFeatures.append(uF)
    movieFeatures.append(uM)
    singular_value = multiply_feature_vectors(uF, uM)

    remainder = remainder.minus(singular_value)

    # sigma /= 4
    # if abs(remainder.mean() - last_difference) < 0.01:
    #   break
    # last_difference = remainder.mean()
    iteration += 1
    print iteration
    # use if have sigma
    # if (real.mean() - remainder.mean()) < 0.8:
    #   break
  return userFeatures, movieFeatures


test_matrix = get_test_matrix()


uFs, mFs = train_some_features(test_matrix, 10)
savetxt('output_large_matrix.txt', uFs, mFs) #save to txt
savez('output_large_matrix.npz', uFs, mFs) #save to binary uncompressed

#if want to write or print results 1-by-1

# file = open('output_large_matrix.txt', 'w')

# file.write('\noriginal matrix' + '\n' + str(test_matrix))
# for singular in range(len(uFs)):
#   # print 'user feature vector '+ str(singular), uFs[singular]
#   # print 'movie feature vector '+ str(singular), mFs[singular]
#   singular_value = multiply_feature_vectors(uFs[singular], mFs[singular])
#   # print singular, singular_value
#   file.write('\n'+ str(singular))
#   file.write('\nuser feature vector ' + '\n' + str(uFs[singular]))
#   file.write('\nmovie feature vector '+ '\n' + str(mFs[singular]))
#   file.write('\nsingular value ' + '\n' + str(singular_value))
#   file.write('\n')
#   # diff = test_matrix.minus(singular_value).mean()
#   # file.write('\ndifference' + str(diff))
#   # print 'difference', diff

# file.close()

#minimized function calls 
#had sigma that was unnecessary (?)
#numpy matrix takes much less memory than anything else


