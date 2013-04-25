

file = open('../data/ml-10M100K/movies.dat')
new_file = open('../data/ml-10M100K/matrix_movies.dat', 'w')

for i in range (10681):
	for line in file:
		new_file.write(str(i) + '::' +str(line))
		i += 1

new_file.close()
file.close()