all: ratings_data

ratings_data:
	@[ -e mdata/ml-10M100K/ ] ||\
		(cd data && wget http://www.grouplens.org/sites/www.grouplens.org/external_files/data/ml-10m.zip &&\
		unzip ml-10m.zip) && echo "got ratings data"