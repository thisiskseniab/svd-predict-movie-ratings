
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

def init_feature_vectors(width, height):
  # set feature vectors to initial
  userFeature = [initial] * width
  movieFeature = [initial] * height
  return userFeature, movieFeature


def multiply_feature_vectors(userFeature, movieFeature):
  width = len(userFeature)
  height = len(movieFeature)
  result = Matrix(width, height, 0)
  for x in range(result.width):
    for y in range(result.height):
      result.set(x, y, userFeature[x] * movieFeature[y])
  return result

def train_one_feature(real): #sigma = 0.01
  cycles = 0
  max_cycles = 600
  uF, mF = init_feature_vectors(real.width, real.height)
  while True:
    cycles += 1
    # file.write('\n'+ str(cycles) + '\n')
    predicted = multiply_feature_vectors(uF, mF)
    # file.write(str(predicted) + '\n')
    # errors = real.minus(predicted )
    # file.write('\n'+str(errors.mean()) + '\n')
    if cycles == max_cycles: #errors.mean() < sigma or 
      # print cycles
      break
    else:
      #do i multiply errors by lrate 
      # errors.times(lrate)
      for w in range(real.width):
        for h in range(real.height):
          # print 'w', w
          # print 'h', h
          # print 'real rating', real.index(w, h)
          # file.write('real rating' + str(real.index(w, h)) + '\n')
          # print 'predicted rating', predicted.index(w,h)
          # file.write('predicted rating' + str(predicted.index(w, h)) + '\n')

          #I thought that error has to be an absolute value, but it was throwing the results off 
          #increasing the vectors all the time instead of correcting values of vectors 
          error = (real.index(w, h) - predicted.index(w, h)) * lrate 


          # file.write('error' + str(error) + '\n')

          # error = abs(lrate * (predicted.index(w, h) - predict_rating(real, h, w)))
          uv = uF[w]

          uF[w] += error * mF[h]

          # file.write('uF[w]' + str(uF[w]) + '\n')

          mF[h] += error * uv

          # file.write('mF[h]' + str(mF[h]) + '\n')
  # print uF, mF
  # file.write('uF, mF' + str(uF) + str(mF) + '\n')
  # print multiply_feature_vectors(uF, mF)
  # file.write('multiplied feature vectors' + str(multiply_feature_vectors(uF, mF)) + '\n')
  # print predicted
  return uF, mF


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
    # file.write('\nsingularvalue'+ str(singular_value))
    remainder = remainder.minus(singular_value)
    # file.write('\nremainder' + str(remainder))

    # userFeatures.append(uF)
    # movieFeatures.append(uM)
    # sigma /= 4
    # if abs(remainder.mean() - last_difference) < 0.01:
    #   break
    # last_difference = remainder.mean()
    iteration += 1
    print iteration
    # print last_difference
    # if (real.mean() - remainder.mean()) < 0.8:
    #   break
  # print 'features', userFeatures, movieFeatures
  return userFeatures, movieFeatures

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
