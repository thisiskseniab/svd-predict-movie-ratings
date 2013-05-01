#might be helpful to have a class that uses index (instead of multiplying all vectors) to get a prediction for a particular movie


class UnrealizedMatrix:
	def __init__(self):
		pass
	def getUnrealMatrix(self, featurevector1, featurevector2):
		self.featurevector1 = featurevector1
		self.featurevector2 = featurevector2
	#should I use ids or indexes?	
	def index(self, user_index, movie_index):
		return self.featurevector1[user_index] * self.featurevector2[movie_index]

