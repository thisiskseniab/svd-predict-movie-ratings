#! /usr/bin/env pypy

import redis
import json

import sys

# quick hack
sys.path.append('../app/')
import model

FEATURE_COUNT = 5
IPF = 25


redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)


def load_feature_from_redis(feature_number, feature_type, ipf=IPF):
	key = 'f' + str(feature_number) + feature_type[0] + str(ipf) + 'ipf'
	feature_value = redis_server.get(key)
	feature = json.loads(feature_value)
	return feature

def load_fvs_from_redis():
	return [load_feature_from_redis(i, 'user') for i in xrange(FEATURE_COUNT)], [load_feature_from_redis(i, 'movie') for i in xrange(FEATURE_COUNT)]	


# files are named like feature3_vector_movie.json
# number is feature number, kind is movie or user
def load_json_file(number, kind):
	with open('../data/feature'+ str(number) +'_vector_' + kind + '.json', 'r') as fv_file:
		return json.load(fv_file)


# user first then movie as always
def load_fvs_from_json_file():
	return [load_json_file(i, 'user') for i in xrange(FEATURE_COUNT)], [load_json_file(i, 'movie') for i in xrange(FEATURE_COUNT)]


# return a dictionary that maps a user_index to an array of movie_indexes
# this will be very large in memory, good reason to use pypy
def get_existing_ratings_from_file():
	existing_ratings = {}
	user_index_to_id, movie_id_to_index = load_json_indexes()
	user_id_to_index = load_user_id_to_index_index()
	with open("../data/ml-10M100K/ratings.dat") as ratings_file:
		for line in ratings_file:
			line = line.split('::')
			user_id = int(line[0])
			movie_id = int(line[1])
			user_index = user_id_to_index[user_id]
			movie_index = movie_id_to_index[movie_id]
			cur_user_ratings = existing_ratings.get(user_index, [])
			cur_user_ratings.append(movie_index)
			existing_ratings[user_index] = cur_user_ratings
	return existing_ratings 


# uses the model module
def write_one_user_prediction_to_sql(user_index, session, existing_ratings):
	prediction_dict = get_unfiltered_user_prediction_dict(user_index)
	# now we need to filter it by existing_ratings
	for movie_index in existing_ratings[user_index]:
		prediction_dict[movie_index] = 0

	count = 0
	for movie_index, rating in sorted(prediction_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		count += 1
		if count > 50:
			break
		prediction = model.Prediction(user_index, movie_index, int(rating)) # ?
		session.add(prediction)
		if count % 10 == 0:
			session.commit()

	session.commit()


# uses the model module
def write_all_user_predictions_to_sql():
	# user_index_to_id, movie_id_to_index = load_json_indexes()
	# user_id_to_index = load_user_id_to_index_index()
	session = model.connect()
	existing_ratings = get_existing_ratings_from_file()
	for user_index in xrange(70000): #fixme
		write_one_user_prediction_to_sql(user_index, session, existing_ratings)


# this will actually work: http://docs.python.org/2/library/stdtypes.html#dict.items
def fix_json_string_keys(d):
	return dict(zip([int(k) for k in d.keys()], [int(v) for v in d.values()]))

# load only the indexes needed in this context
# (index is a confusing term)
def load_json_indexes():
  with open('../data/ml-10M100K/index_to_user_id.json', 'r') as user_file:
    user_index_to_id = fix_json_string_keys(json.load(user_file))
  with open('../data/ml-10M100K/movie_id_to_index.json', 'r') as movie_file:
    movie_id_to_index = fix_json_string_keys(json.load(movie_file))
  return user_index_to_id, movie_id_to_index

def load_user_id_to_index_index():
  with open('../data/ml-10M100K/user_id_to_index.json', 'r') as user_file:
    return fix_json_string_keys(json.load(user_file))

def get_unfiltered_user_prediction_dict(user_index):
	# get a list of ratings ordered by movie_index
	predictions = build_user_prediction_row(user_index)
	# put into a dictionary, it is easier
	# movie_index -> rating, then sort by value later
	return dict(zip(xrange(len(predictions)), predictions))


def get_user_prediction_dict(user_index):
	# get a list of ratings ordered by movie_index
	predictions = build_user_prediction_row(user_index)
	already_rated_movies = get_user_rated_movie_indexes_from_file(user_index)
	# set the existing ratings to 0 in the predictions so they're ignored
	for i in xrange(len(already_rated_movies)):
		print "already", already_rated_movies[i], predictions[already_rated_movies[i]] # temp
		predictions[already_rated_movies[i]] = 0

	# put into a dictionary, it is easier
	# movie_index -> rating, then sort by value later
	return dict(zip(xrange(len(predictions)), predictions))
	

# return a list of movie_indexes
def predict_users_top_50_ratings(user_index):
	prediction_dict = get_user_prediction_dict(user_index)
	# print 'pd', prediction_dict
	top_predictions = []
	count = 0
	# find the movie indexes with the highest ratings, or sort the movie_indexes by rating
	for movie_index, rating in sorted(prediction_dict.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		# print movie_index
		top_predictions.append(movie_index)
		count += 1
		if count >= 50:
			break
	return top_predictions


# the file contains movie ids and user ids so we need the indexes to convert
# return a list of movie indexes that the user has rated
def get_user_rated_movie_indexes_from_file(user_index):
	# look up the user's id in the reverse index
	user_index_to_id, movie_id_to_index = load_json_indexes()
	rated_movie_indexes = []
	ratings = {}
	# print user_index_to_id
	# print 'id from index', user_index_to_id[user_index], type(user_index_to_id[user_index])
	with open("../data/ml-10M100K/ratings.dat") as ratings_file:
		for line in ratings_file:
			line = line.split('::')
			user_id = int(line[0])
			if user_index_to_id[user_index] == user_id:
				# a user can rate a movie only once
				rated_movie_indexes.append(movie_id_to_index[int(line[1])])
				ratings[movie_id_to_index[int(line[1])]] = float(line[2])
				#print 'id', user_id
	print "ratings", ratings # temp
	return rated_movie_indexes


def build_user_prediction_row(user_index):
	#user_features, movie_features = load_fvs_from_json_file()
	user_features, movie_features = load_fvs_from_redis()

	# make an empty row to start
	total_prediction_row = [0] * len(movie_features[0])
	# sum all the user prediction rows from every feature
	for feature_number in xrange(FEATURE_COUNT):
		feature_prediction_row = build_user_prediction_row_from_one_feature(user_index, user_features, movie_features, feature_number)
		# print len(movie_features)
		# print feature_prediction_row
		for i in xrange(len(feature_prediction_row)):
			total_prediction_row[i] += feature_prediction_row[i]
	return total_prediction_row


def build_user_prediction_row_from_one_feature(user_index, user_features, movie_features, feature_number):
	return [user_features[feature_number][user_index] * mfv for mfv in movie_features[feature_number]]


def movie_index_to_movie_name_genre(movie_index):
	_, movie_id_to_index = load_json_indexes()
	with open('../data/ml-10M100K/movies.dat') as movie_file:
		for line in movie_file:
			line = line.split('::')

			movie_id = int(line[0])

			# print 'on id', movie_id, type(movie_id)
			# print 'id to index', movie_id_to_index[movie_id], type(movie_id_to_index[movie_id])
			# print 'looking for index', movie_index, type(movie_index)

			if movie_id_to_index[movie_id] == movie_index:
				movie_name = line[1]
				movie_genre = line[2]
				# done
				return movie_name, movie_genre
	# if you get here the value will be None
	# print "could not find movie_index", movie_index


def get_user_predictions(user_index):
	top10 = predict_users_top_50_ratings(user_index)
	actual = get_user_rated_movie_indexes_from_file(user_index)

	top10 = [movie_index_to_movie_name_genre(mi) for mi in top10]
	actual = [movie_index_to_movie_name_genre(mi) for mi in actual]

	print "top 10", top10, '\n', "actual", actual


def main(args):
	# print args
	if len(args) > 1 and args[1] == '--sql':
		print 'writing predictions to sql for all users...'
		write_all_user_predictions_to_sql()
	else:
		wanted_user_indexes = [500, 5000, 50000]
		for user_index in wanted_user_indexes:
			get_user_predictions(user_index)

if __name__ == "__main__":
	main(sys.argv)
