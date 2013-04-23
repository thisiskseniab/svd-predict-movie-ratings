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
['30', '590', '5', '876529220']

def map_ratings():
  ratings = open('../data/ml-10M100K/ratings_25.dat')
  count_users = 0
  count_movies = 0
  mapped_ratings = {}
  users = []
  movies = []

  for line in ratings:
    values = line.split('::')
    print values
    if values[0] in users:
      pass
    else:
      users.append(values[0])
      count_users += 1
    if values[1] in movies:
      pass
    else: 
      movies.append(values[1])
      count_movies += 1

    mapped_ratings[(int(values[0]),int(values[1]))] = float(values[2])

  print mapped_ratings
  return mapped_ratings

def get_test_matrix():
  t = Matrix(4, 5, 0) #71567, 10681 139
  for x in range(t.width):
    for y in range(t.height):
      t.set(x, y, random.randrange(1, 5, 1))
  #t.values = [1,2,3,4,5] * 1000 #200010
  return t

def set_matrix():
  ratings = open('../data/ml-10M100K/ratings_25.dat')
  count_users = 0
  count_movies = 0
  mapped_ratings = {}
  users = []
  movies = []

  for line in ratings:
    values = line.split('::')
    print values
    if values[0] in users:
      pass
    else:
      users.append(values[0])
      count_users += 1
    if values[1] in movies:
      pass
    else: 
      movies.append(values[1])
      count_movies += 1

    mapped_ratings[(int(values[0]),int(values[1]))] = float(values[2])

  print mapped_ratings
  print map_ratings.keys()

  t = Matrix(count_users, count_movies, )


# lala = map_ratings()
lalala = set_matrix()
# i want to count the movies
# count the users
# make arrays that map the movie ids -> movie indexes and user ids -> user indexes
# write a function that takes a rating and inserts it into a matrix at an appropriate point