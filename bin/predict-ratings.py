#! /usr/bin/env pypy

# UserID::MovieID::Rating::Timestamp
# 1::122::5::838985046

def get_ratings():

	ratings_lines = open('../data/ml-10M100K/ratings_10.dat')
	ratings = [] #[[0,0,0]] * 10 
	predictions = []
	records = []
	lrate = 1
	i = 0
	user = 0.1 #int(record[0])
	movie = 0.1 #int(record[1])
	user_val = 0
	movie_val = 0
	for line in ratings_lines:
		record = line.split('::')
		rating = int(record[2])*1000
		ratings.append(rating)
		prediction = (movie[i] * user[i]) * 1000
		predictions.append(prediction)
		i += 1

	for rating in ratings:
		error = (rating - prediction) * lrate
		user += error  #user value ratings[i][0]
		records.append(user)
		movie += error # movie value ratings[i][1]
		records.append(movie)
		records.append(rating)
		i += 1
	print ratings, predictions, records


def train_for_features():
	pass
	#for feature in range(40):
		#call get_ratings function
		#substract the matrix that is the result of get_ratings from the original ratings
		#save the result 

	#as a result, have 40 matricies which represent 40 features that have effect on user's rating 
	# - from the heaviest to the lightest *by effect*

def main():
	get_ratings()
	# train_for_features()

if __name__ == "__main__":  
	main()
