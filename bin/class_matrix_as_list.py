class Matrix:
  def __init__(self, height, width, i):
    self.height = height
    self.width = width
    self.values = [i] * width * height

  # the index function will work like m[2][3]
  def index(self, x, y):
    return self.values[ (y * self.width) + x ]

  def set(self, x, y, value):
    self.values[ (y * self.width) + x ] = value
 
  # unlike times, minus will not alter self
  def minus(self, other_matrix):
    assert(self.width == other_matrix.width)
    assert(self.height == other_matrix.height)
    result = Matrix(self.width, self.height, 0)
    for x in range(self.width):
      for y in range(self.height):
        result.set(x, y, self.index(x,y) - other_matrix.index(x, y))
    return result

  def times(self, coefficient):
    temp = []
    for value in self.values:
      value = value * coefficient
      temp.append(value)

    self.values = temp

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