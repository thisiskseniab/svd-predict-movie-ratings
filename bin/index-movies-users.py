
import json

# the result of running this is:
# two files:
# * a file containing a json object which is the index from movie id -> index
# * a file containing a json object which is the index from index -> id
# TODO: indexing users

# {
#   <movie id>: <movie index>,
#   ...
# }

# type is either 'movie' or 'user'
def build_index_files(filename, type):
  # we will do a single pass
  # this takes as long as counting from 1 to 65k or whatever
  input_file = open(filename)

  id_to_index = {}
  index_to_id = {}

  index = 0
  for line in input_file:
    id = int(line.split('::')[0])
    if not id_to_index.has_key(id):
      id_to_index[id] = index
      index_to_id[index] = id
      index += 1

  # now we have two objects, let's write them both to files
  with open('../data/ml-10M100K/'+ type +'_id_to_index.json', 'w') as id_file:
    json.dump(id_to_index, id_file, indent=2, sort_keys=True)

  with open('../data/ml-10M100K/index_to_'+ type +'_id.json', 'w') as index_file:
    json.dump(index_to_id, index_file, indent=2, sort_keys=True)


build_index_files('../data/ml-10M100K/movies.dat' , 'movie')
build_index_files('../data/ml-10M100K/ratings.dat', 'user')
