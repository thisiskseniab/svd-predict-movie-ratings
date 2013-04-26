	-- schema.sql

create table Ratings (
    user_id INTEGER PRIMARY KEY,
    movie_id INTEGER,
    rating INTEGER,
    time INTEGER
);
create table Users (
    user_id INTEGER PRIMARY KEY,
    age INTEGER,
    gender VARCHAR(1),
    occupation VARCHAR(64),
    zip_code INTEGER,
    email VARCHAR(128),
    password VARCHAR(128),
);

create table Movies (
	matrix_movie_id INTEGER PRIMARY KEY,
	movie_id INTEGER,
	movie_title VARCHAR(128),
	year INTEGER,
	genre VARCHAR(256)
);
