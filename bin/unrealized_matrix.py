#might be helpful to have a class that uses index (instead of multiplying all vectors) to get a prediction for a particular movie


class UnrealizedMatrix:
	def __init__(self):
		pass
	def getUnrealMatrix(self, fv1, fv2):
		self.fv1 = fv1
		self.fv2 = fv2
	def index(self, w, h):
		return self.fv1 * self.fv2

