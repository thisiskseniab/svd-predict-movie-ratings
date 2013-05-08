#! /usr/bin/env pypy

import redis
import json


# the IPF of the feature vectors we are importing
IPF = 400 # 10?

redis_server = redis.StrictRedis(host='localhost', port=6379, db=0)


def write_feature_to_redis(feature, feature_number, feature_type, ipf):
	key = 'f' + str(feature_number) + feature_type[0] + str(ipf) + 'ipf'
	redis_server.set(key, json.dumps(feature, indent=4))


# json files are named like feature0_vector_movie.json
def load_feature_file(feature_number, feature_type):
	filename = 'feature' + str(feature_number) + '_vector_' + feature_type + '.json'
	with open('../data/400ipf/' + filename, 'r') as infile:
		return json.load(infile)


def main():
	for feature_number in xrange(4):
		for feature_type in ['user', 'movie']:
			feature = load_feature_file(feature_number, feature_type)
			write_feature_to_redis(feature, feature_number, feature_type, IPF)


if __name__ == "__main__":
    main()	